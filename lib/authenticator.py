#
# HamperAuthenticator is the class to handle the authentication part of the provisioning portal.
# Instantiate with the email and password you want, it'll pass back the cookie jar if successful,
# or an error message on failure
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class HamperAuthenticator(object):

	def __init__(self, email, password):
		super(HamperAuthenticator, self).__init__()
		self.email 	  = email
		self.password = password

	def sign_in(self, driver):
		# Open the profile URL. This will forward to the sign in page if session is invalid
		driver.get("https://developer.apple.com/account/ios/profile/")

		email_element = driver.find_element_by_name("appleId")
		email_element.send_keys(self.email)

		password_element = driver.find_element_by_name("accountPassword")
		password_element.send_keys(self.password)

		driver.find_element_by_id("submitButton2").click()
		
		return driver