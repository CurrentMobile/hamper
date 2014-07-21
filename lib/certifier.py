#
# HamperCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by HamperAuthenticator and the CSR file path to use. 
# HamperCertifier will then go off and generate a distribution certificate on the account.
#

from error import HamperError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import time


class HamperCertifier(object):

	#
	# Set up constants for the specific types of certificate.
	# Use these when calling generate_certificate() to pick the type of cert to create
	#
	HCCertificateTypeDevelopment  	  = 0
	HCCertificateTypeDevelopmentPush  = 1
	HCCertificateTypeDistribution 	  = 2
	HCCertificateTypeDistributionPush = 3

	def __init__(self, csr_path):
		super(HamperCertifier, self).__init__()
		# self.driver = driver
		self.csr_path = csr_path

	#
	# Shortcut methods to create the desired certificate
	# instead of calling generate_certificate with a bunch of params
	#
	def generate_development_certificate(self, driver, app_id):
		return self.generate_certificate(driver, certificate_type=HCCertificateTypeDevelopment)
	
	def generate_development_push_certificate(self, driver, app_id):
		return self.generate_certificate(driver, certificate_type=HCCertificateTypeDevelopmentPush)

	def generate_distribution_certificate(self, driver):
		return self.generate_certificate(driver, certificate_type=HCCertificateTypeDistribution)
	
	def generate_distribution_push_certificate(self, driver):
		return self.generate_certificate(driver, certificate_type=HCCertificateTypeDistribution)


	def generate_certificate(self, driver, certificate_type=HCCertificateTypeDistributionPush):
		self.pick_certificate_type(driver, certificate_type)
		self.confirm_csr_instructions(driver)

		return self.generate_and_download_certificate(driver)


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

	def confirm_csr_instructions(self, driver):
		# ---------	
		#	Browser is now at this page:
		#	http://i.imgur.com/xaeAm2z.png
		# ---------

		# Wait until the continue button is clickable
		time.sleep(0.2)

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")

		# Click the Continue button
		continue_button_element.click()

	def generate_and_download_certificate(self, driver):
		# -------
		#	Browser is now at this page:
		#	http://i.imgur.com/xzeQEZA.png
		#
		#	We now upload the CSR at the provided filepath.
		# -------

		# Wait until the upload field is clickable
		time.sleep(0.2)
		
		# Set the file being uploaded to the CSR provided in the initialiser
		file_upload_field = driver.find_element_by_name("upload")
		file_upload_field.send_keys(self.csr_path)

		# Find and click the submit button
		generate_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
		generate_button_element.click()
		
		# Have the browser wait until the downloadForm is visible (this contains the download button & link)
		wait = WebDriverWait(driver, 20)
		wait.until(lambda driver: driver.find_element_by_class_name('downloadForm'))

		# Find the download button, grab the download URL		
		download_button_element = driver.find_element_by_css_selector(".button.small.blue")
		download_url = download_button_element.get_attribute("href")
	
		# Return the download URL
		return download_url