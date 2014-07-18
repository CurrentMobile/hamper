#
# HamperCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by HamperAuthenticator and the CSR file path to use. 
# HamperCertifier will then go off and generate a distribution certificate on the account.
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait

class HamperCertifier(object):
	def __init__(self, csr_path):
		super(HamperCertifier, self).__init__()
		# self.driver = driver
		self.csr_path = csr_path			

	def generate_certificate(self, driver):

		# This will trigger the provisioning portal to load this page: i.imgur.com/8RmehDm.png
		driver.get("https://developer.apple.com/account/ios/certificate/certificateCreate.action?formID=27276876")

		# Select the radio button to create a distribution certificate
		radio_button = driver.find_element_by_id("type-iosNoOCSP")

		# Click the radio button
		radio_button.click()

		# Locate the submit button on the page
		submit_button_element = driver.find_element_by_class_name("submit")

		# Click the submit button
		submit_button_element.click()

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


