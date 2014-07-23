#
# HamperAuthenticator is the class to handle the authentication part of the provisioning portal.
# Instantiate with the email and password you want, it'll pass back the cookie jar if successful,
# or an error message on failure
#
from helpers.driver import HamperDriver
from helpers.error import HamperError

from termcolor import colored

class HamperAuthenticator(object):

	def __init__(self):
		super(HamperAuthenticator, self).__init__()

	def sign_in(self, email=None, password=None):
		print colored("Authenticating user...", "blue")
		
		# If no login credentials were provided
		if not email or not password:
			raise Exception(HamperError(HamperError.HECodeLogInError, "Either the email and/or password wasn't provided. Call 'hamper auth login' with the login credentials."))

		# Grab the HamperDriver singleton
		driver = HamperDriver()

		# Open the profile URL. This will forward to the sign in page if session is invalid
		driver.get("https://developer.apple.com/account/ios/profile/")

		email_element = driver.find_element_by_name("appleId")
		email_element.send_keys(email)

		password_element = driver.find_element_by_name("accountPassword")
		password_element.send_keys(password)

		driver.find_element_by_id("submitButton2").click()

		if len(driver.find_elements_by_class_name("dserror")) > 0:
			raise Exception(HamperError(HamperError.HECodeLogInError, driver.find_element_by_class_name("dserror").get_attribute("innerHTML"))) 
		else:
			print colored("User successfully authenticated.", "green")