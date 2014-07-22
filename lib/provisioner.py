#
# HamperProvisioner is the class to handle the creation and downloading of provisioning profiles
# By default it will sign a development profile with all the available certificates for that type. It will also auto-select all devices to be provisioned.
# By default it will sign a distribution profile with the first profile in the list. You can change this by specifying
# the expiration date of the profile to be used.
#

from helpers.error import HamperError
from helpers.driver import HamperDriver

from selenium.webdriver.support.ui import WebDriverWait

import time

class HamperProvisioner(object):

	HPProfileTypeDevelopment  = 0
	HPProfileTypeAppStore = 1
	HPProfileTypeAdHoc = 2
	
	def __init__(self):
		super(HamperProvisioner, self).__init__()



	def generate_provisioning_profile(self, profile_type, app_id, profile_name):
		self.pick_profile_type(profile_type)
		self.select_app_id(app_id)
		self.pick_development_signing_certificate()
		self.pick_provisioned_devices()
		self.enter_profile_name(profile_name)
		print self.download_provisioning_profile()

	def pick_profile_type(self, profile_type):
		
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

	def pick_provisioned_devices(self):
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
		# Grab the HamperDriver singleton
		driver = HamperDriver()

		time.sleep(0.2)

		profile_name_element = driver.find_element_by_name("provisioningProfileName")
		profile_name_element.send_keys(profile_name)

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the continue button
		continue_button_element.click()

	def download_provisioning_profile(self):
		# Grab the HamperDriver singleton
		driver = HamperDriver()

		# Have the browser wait until the downloadForm is visible (this contains the download button & link)
		wait = WebDriverWait(driver, 30)
		wait.until(lambda driver: driver.find_element_by_class_name("downloadForm"))

		# Find the download button, grab the download URL		
		download_button_element = driver.find_element_by_css_selector(".button.small.blue")
		download_url = download_button_element.get_attribute("href")
	
		# Return the download URL
		return download_url
