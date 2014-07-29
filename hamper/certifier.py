#
# HamperCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by HamperAuthenticator and the CSR file path to use. 
# HamperCertifier will then go off and generate a distribution certificate on the account.
#

from helpers.error import HamperError
from helpers.driver import HamperDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from termcolor import colored
import urllib

class HamperCertifier(object):

	#
	# Set up constants for the specific types of certificate.
	# Use these when calling generate_certificate() to pick the type of cert to create
	#
	HCCertificateTypeDevelopment  	  = 0
	HCCertificateTypeDevelopmentPush  = 1
	HCCertificateTypeDistribution 	  = 2
	HCCertificateTypeDistributionPush = 3

	def __init__(self):
		super(HamperCertifier, self).__init__()

	#
	# Shortcut methods to create the desired certificate
	# instead of calling generate_certificate with a bunch of params
	#
	def generate_development_certificate(self, csr_file, cert_path):
		return self.generate_certificate(certificate_type=HamperCertifier.HCCertificateTypeDevelopment, csr_path=csr_file, certificate_path=cert_path)
	
	def generate_development_push_certificate(self, application_id, csr_file, cert_path):
		return self.generate_certificate(certificate_type=HamperCertifier.HCCertificateTypeDevelopmentPush, app_id=application_id, csr_path=csr_file, certificate_path=cert_path)

	def generate_distribution_certificate(self, csr_file, cert_path):
		return self.generate_certificate(certificate_type=HamperCertifier.HCCertificateTypeDistribution, csr_path=csr_file, certificate_path=cert_path)
	
	def generate_distribution_push_certificate(self, application_id, csr_file, cert_path):
		return self.generate_certificate(certificate_type=HamperCertifier.HCCertificateTypeDistributionPush, app_id=application_id, csr_path=csr_file, certificate_path=cert_path)
	#
	# Main method to run the submethods to generate the certificate.
	#
	def generate_certificate(self, certificate_type=HCCertificateTypeDistribution, app_id="", csr_path="", certificate_path=""):

		print colored("Generating certificate...", "blue")

		# Grab the HamperDriver singleton
		current_driver = HamperDriver()

		print colored("Picking certificate type...", "blue")
		
		# Set the certificate_type property 
		self.pick_certificate_type(current_driver, certificate_type)

		# If we're going to generate a push certificate, we need to specify an app ID.
		# This is an extra step in the Provisioning Profile process
		if certificate_type == HamperCertifier.HCCertificateTypeDevelopmentPush or certificate_type == HamperCertifier.HCCertificateTypeDistributionPush:
			print colored("Selecting application ID...", "blue")
			self.select_app_id(current_driver, app_id)

		print colored("Confirming CSR instructions...", "blue")

		# Confirm the CSR generation instructions
		self.confirm_csr_instructions(current_driver)
		
		print colored("Generating certificate (this could take a minute)...", "blue")
		
		# Generate, wait, and download the actual certificate. Return the URL.
		download_url = self.confirm_certificate_generation(current_driver, csr_path)
		
		if download_url and len(download_url) > 0:
			print colored("Certificate successfully generated.", "green")
			
			print colored("Downloading certificate (this could take a minute)...", "blue")
			
			# Download the certificate to the user-defined path
			self.download_certificate(current_driver, download_url, certificate_path)

			print colored("Certificate successfully downloaded (" + certificate_path + ").", "green")

		else:
			raise Exception(HamperError(1, "Could not generate certificate and/or certificate download URL."))

	def pick_certificate_type(self, driver, certificate_type):
		# This will trigger the provisioning portal to load this page: i.imgur.com/8RmehDm.png
		driver.get("https://developer.apple.com/account/ios/certificate/certificateCreate.action?formID=27276876")

		# Create a var to store the radio button's ID in (will depend on the cert type being requested)
		button_id = ""

		# Check the cert type parameter, set the button's ID accordingly
		if certificate_type == HamperCertifier.HCCertificateTypeDevelopment:
			button_id = "type-development"
		elif certificate_type == HamperCertifier.HCCertificateTypeDevelopmentPush:
			button_id = "type-sandbox"
		elif certificate_type == HamperCertifier.HCCertificateTypeDistribution:
			button_id = "type-iosNoOCSP"
		elif certificate_type == HamperCertifier.HCCertificateTypeDistributionPush:
			button_id = "type-production"

		radio_button = driver.find_element_by_id(button_id)

		is_disabled = radio_button.get_attribute("disabled")
		
		# Check whether the radio button is disabled.
		# This could be disabled because the account already has a few certs of that type
		if is_disabled:
			raise Exception(HamperError(HamperError.HECodeDisabledCertificateType, "Certificate type is disabled. This could be because you already have multiple of that type of cert. Try deleting one certificate of this type."))

		# Click the radio button
		radio_button.click()

		# Locate the submit button on the page
		submit_button_element = driver.find_element_by_class_name("submit")

		# Click the submit button
		submit_button_element.click()

	def select_app_id(self, driver, app_id):
		# ---------	
		#	Browser is now at this page:
		#	http://i.imgur.com/D4bmbAi.png
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

	def confirm_csr_instructions(self, driver):
		# ---------	
		#	Browser is now at this page:
		#	http://i.imgur.com/xaeAm2z.png
		# ---------

		time.sleep(0.2)

		# Wait until the continue button is clickable
		wait = WebDriverWait(driver, 20)
		wait.until(lambda driver: driver.find_element_by_class_name("submit"))

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_class_name("submit")

		# Click the Continue button
		continue_button_element.click()

	def confirm_certificate_generation(self, driver, csr_path):
		# -------
		#	Browser is now at this page:
		#	http://i.imgur.com/xzeQEZA.png
		#
		#	We now upload the CSR at the provided filepath.
		# -------

		# Wait until the upload field is clickable
		wait = WebDriverWait(driver, 20)
		wait.until(lambda driver: driver.find_element_by_name("upload"))

		# Set the file being uploaded to the CSR provided in the initialiser
		file_upload_field = driver.find_element_by_name("upload")
		file_upload_field.send_keys(csr_path)

		# Find and click the submit button
		generate_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
		generate_button_element.click()
		
		# Have the browser wait until the downloadForm is visible (this contains the download button & link)
		wait = WebDriverWait(driver, 30)
		wait.until(lambda driver: driver.find_element_by_class_name('downloadForm'))

		# Find the download button, grab the download URL		
		download_button_element = driver.find_element_by_css_selector(".button.small.blue")
		download_url = download_button_element.get_attribute("href")
	
		# Return the download URL
		return download_url

	def download_certificate(self, driver, download_url, cert_path):

		# Create a URLOpener object
		opener = urllib.URLopener()
		
		# Grab all the cookies from Selenium
		all_cookies = driver.get_cookies()

		# Loop through each cookie
		for cookie in all_cookies:
			# Add the cookie to the URLOpener instance
			opener.addheaders.append(('Cookie', cookie['name'] + "=" + cookie['value']))

		# Save the certificate file into the user-defined path
		opener.retrieve(download_url, cert_path)