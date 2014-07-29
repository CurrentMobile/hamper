#
# HamperProvisioner is the class to handle the creation and downloading of provisioning profiles.
#
# By default it will sign a development profile with all the available certificates for that type. It will also auto-select all devices to be provisioned.
# By default it will sign a distribution profile with the first profile in the list. You can change this by specifying the expiration date of the profile 
# to be used.
#

from helpers.error import HamperError
from helpers.driver import HamperDriver
from helpers.date import HamperDate

from selenium.webdriver.support.ui import WebDriverWait

import time

import urllib

# For CLI

from termcolor import colored

class HamperProvisioner(object):

	HPProfileTypeDevelopment  = 0
	HPProfileTypeAppStore = 1
	HPProfileTypeAdHoc = 2
	
	def __init__(self):
		super(HamperProvisioner, self).__init__()

	def generate_development_profile(self, app_id, profile_name, profile_path):
		return self.generate_provisioning_profile(HamperProvisioner.HPProfileTypeDevelopment, app_id, profile_name, profile_path)

	def generate_app_store_profile(self, app_id, profile_name, profile_path, expiration_date=None):
		return self.generate_provisioning_profile(HamperProvisioner.HPProfileTypeAppStore, app_id, profile_name, profile_path, date=expiration_date)

	def generate_adhoc_profile(self, app_id, profile_name, profile_path, expiration_date=None):
		return self.generate_provisioning_profile(HamperProvisioner.HPProfileTypeAdHoc, app_id, profile_name, profile_path, date=expiration_date)

	def generate_provisioning_profile(self, profile_type, app_id, profile_name, profile_path, date=None):
		print colored("Generating provisioning profile...", "blue")

		self.pick_profile_type(profile_type)
		self.select_app_id(app_id)

		if profile_type == HamperProvisioner.HPProfileTypeAppStore or profile_type == HamperProvisioner.HPProfileTypeAdHoc:
			self.pick_distribution_signing_certificate(date)
		else:
			self.pick_development_signing_certificate()

		# If we're generating a development or adhoc profile, we need to pick the provisioned devices
		if profile_type == HamperProvisioner.HPProfileTypeDevelopment or profile_type == HamperProvisioner.HPProfileTypeAdHoc:
			self.pick_provisioned_devices()

		self.enter_profile_name(profile_name)

		return self.download_provisioning_profile(profile_path)

	def pick_profile_type(self, profile_type):
		print colored("Picking profile type...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		# This will trigger the provisioning portal to load this page: i.imgur.com/tAz1lHH.png
		driver.get("https://developer.apple.com/account/ios/profile/profileCreate.action")

		# Create a var to store the radio button's ID in (will depend on the cert type being requested)
		button_id = ""

		# Check the cert type parameter, set the button's ID accordingly
		if profile_type == HamperProvisioner.HPProfileTypeDevelopment:
			button_id = "type-development"
		elif profile_type == HamperProvisioner.HPProfileTypeAppStore:
			button_id = "type-production"
		elif profile_type == HamperProvisioner.HPProfileTypeAdHoc:
			button_id = "type-adhoc"

		# Find the radio button to select (based on the button_id)
		radio_button = driver.find_element_by_id(button_id)

		# Click the radio button
		radio_button.click()

		# Locate the submit button on the page
		submit_button_element = driver.find_element_by_class_name("submit")

		# Click the submit button
		submit_button_element.click()

	def select_app_id(self, app_id):
		print colored("Selecting app ID...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		# ---------	
		#	Browser is now at this page:
		#	i.imgur.com/coJMLtm.png
		# ---------
		
		time.sleep(0.2)
		
		# Wait until the dropdown is clickable
		wait = WebDriverWait(driver, 20)
		wait.until(lambda driver: driver.find_element_by_name("appIdId"))

		# Select the dropdown list
		select_app_id_dropdown = driver.find_element_by_name("appIdId")

		# Use the xpath to select all the child nodes of the appID dropdown list
		options_list = select_app_id_dropdown.find_elements_by_xpath("./*")

		# Initialise the selected_option
		selected_option = None

		# Loop through the options, check whether the provided appID is 
		# in the dropdown. If it is, set selected_option to that HTML element.
		for option in options_list:
			if app_id in option.text:
				selected_option = option
				break

		# Check whether the option was found (i.e. the selected_option class is of the same type as the selected_app_id_dropdown class)
		if type(selected_option) != type(select_app_id_dropdown):
			# If it wasn't found, throw an exception
			raise Exception(HamperError(HamperError.HECodeInvalidAppID, "The app ID provided (" + app_id + ") could not be found."))

		# If the app ID exists in the list, select it from the dropdown menu
		selected_option.click()

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()

	def pick_development_signing_certificate(self):
		print colored("Picking development certificate...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		time.sleep(0.2)

		# Select the column containing the 'select all' checkbox
		select_all_column = driver.find_element_by_css_selector('.selectAll')

		# Use the xpath to find the input element inside of that column
		select_all_checkbox = select_all_column.find_element_by_xpath('./input')

		# Click the select all checkbox
		select_all_checkbox.click()

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()

	def pick_distribution_signing_certificate(self, date):
		print colored("Picking distribution certfificate...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		time.sleep(0.2)

		# Select the table containing the available certificates
		certificates_table = driver.find_element_by_css_selector('.form.table.distribution')

		# Grab the container of the actual certificates
		rows_div = certificates_table.find_element_by_class_name("rows")

		# Use the xpath to grab all the child elements of rows_div
		# The structure of the contents is like this: gist.github.com/KiranPanesar/a0221c00390b5bdaf5af
		# Where <div class="status">May 22, 2015</div> is the example of an expiration date.
		#
		# We parse out all of the contents so for each certificate there are two divs. One containing the radio button,
		# one for the expiration date.
		available_certificates = rows_div.find_elements_by_xpath("./*")

		# Create a radio_button in the general method scope
		radio_button = None	
		
		if date:
			# Store the stringified version of the date, so it isn't generated on every loop iteration
			date_string = date.readable_date()

			# Loop through the rows in the table
			for i in available_certificates:
				# Check if the current row has the provided expiration date
				if i.get_attribute("innerHTML") == date_string:
					# If it does, get the element ABOVE the current one.
					# Refer back to the structure of the contents (gist.github.com/KiranPanesar/a0221c00390b5bdaf5af)
					current_date_index = available_certificates.index(i)

					# Set the radio button to the above element
					radio_button = available_certificates[current_date_index-1].find_element_by_xpath("./input")

		else:
			# Set the radio button to the above element
			radio_button = available_certificates[0].find_element_by_xpath("./input")

		# If the radio button is None, i.e. no certificate was selected/found, throw an error
		try:
			radio_button.click()
		except Exception, e:
			raise Exception(HamperError(HamperError.HECodeInvalidCertificateExpirationDate, "We could not find a distribution certificate with the specified date (" + date.readable_date() + ") to sign the profile."))
		
		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()


	def pick_provisioned_devices(self):
		print colored("Selecting provisioned devices...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		time.sleep(0.2)

		# Select the column containing the 'select all' checkbox
		select_all_column = driver.find_element_by_css_selector('.selectAll')

		# Use the xpath to find the input element inside of that column
		select_all_checkbox = select_all_column.find_element_by_xpath('./input')

		# Click the select all checkbox
		select_all_checkbox.click()

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()

	def enter_profile_name(self, profile_name):
		print colored("Naming provisioning profile...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		time.sleep(0.2)

		profile_name_element = driver.find_element_by_name("provisioningProfileName")
		profile_name_element.send_keys(profile_name)

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()

	def download_provisioning_profile(self, file_path):
		print colored("Waiting for Apple to generate profile (this could take a minute)...", "blue")

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		# Have the browser wait until the downloadForm is visible (this contains the download button & link)
		wait = WebDriverWait(driver, 30)
		wait.until(lambda driver: driver.find_element_by_class_name("downloadForm"))

		# Find the download button, grab the download URL		
		download_button_element = driver.find_element_by_css_selector(".button.small.blue")
		download_url = download_button_element.get_attribute("href")

		print colored("Provisioning profile successfully generated.", "green")

		print colored("Downloading provisioning profile...", "blue")

		# Create a URLOpener object
		opener = urllib.URLopener()
		
		# Grab all the cookies from Selenium
		all_cookies = driver.get_cookies()

		# Loop through each cookie
		for cookie in all_cookies:
			# Add the cookie to the URLOpener instance
			opener.addheaders.append(('Cookie', cookie['name'] + "=" + cookie['value']))

		# Save the profile file into the user-defined path
		opener.retrieve(download_url, file_path)

		print colored("Profile successfully downloaded (" + file_path + ").", "green")