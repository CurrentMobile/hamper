#
# HamperCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by HamperAuthenticator and the CSR file path to use. 
# HamperCertifier will then go off and generate a distribution certificate on the account.
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
		# Browser is now at this page:
		# http://i.imgur.com/xaeAm2z.png
		# ---------
		driver.get("https://developer.apple.com/account/ios/certificate/certificateCreate.action?formID=65342375")

		# Locate the Continue button on the page
		continue_button_element = driver.find_element_by_class_name("cancel")

		# Click the Continue button
		continue_button_element.click()
