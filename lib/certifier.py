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
		# It will be prefilled to generate a distribution certificate
		driver.get("https://developer.apple.com/account/ios/certificate/certificateCreate.action?formID=27276876")

		submit_button_element = driver.find_element_by_xpath("//input[@class='button small blue right submit'")
		submit_button_element.submit()