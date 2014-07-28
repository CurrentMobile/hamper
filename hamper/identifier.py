#
# HamperIdentifier is the class to handle the creation of the identifiers used in the provisioning portal
# Use this class to create the app ID for your application.
#

from helpers.error import HamperError
from helpers.driver import HamperDriver

from selenium.webdriver.support.ui import WebDriverWait

import time

from termcolor import colored

class HamperIdentifier(object):

	#
	# The enabled services constants. Taken from the 'name' of each item in the provisioning portal.
	#
	HIServiceAppGroups = "APG3427HIY"
	HIServiceAssociatedDomains = "SKC3T5S89Y"
	HIServiceDataProtection = "dataProtectionPermission"
	HIServiceHealthKit = "HK421J6T7P"
	HIServiceHomeKit = "homeKit"
	HIServiceWirelessAccessory = "WC421J6T7P"
	HIServiceiCloud = "iCloud"
	HIServiceInterAppAudio = "IAD53UNK2F"
	HIServicePassbook = "pass"
	HIServicePushNotifications = "push"
	HIServiceVPNConfiguration = "V66P55NK2I"

	def __init__(self):
		super(HamperIdentifier, self).__init__()
		
		self.driver = HamperDriver()

	#
	# Public method to be called to generate an app ID
	#
	def generate_app_id(self, name, bundle_id, app_services=[]):
		print colored("Generating app ID...", "blue")

		# Point the driver to the creation page
		self.driver.get("https://developer.apple.com/account/ios/identifiers/bundle/bundleCreate.action")
		
		# Call the internal methods to fill out the options
		self.enter_app_name(name)
		self.enter_bundle_identifier(bundle_id)
		self.select_enabled_app_services(app_services)

		# Click the continue button
		self.click_continue_button()

		# Confirm the app ID creation
		self.click_submit_button()

		print colored("App ID successfully generated.", "green")
	
	# ------
	# Internal methods to process the app ID flow
	# ------

	# Method to fill out the app's name
	def enter_app_name(self, name):
		app_name_element = self.driver.find_element_by_name("appIdName")
		app_name_element.send_keys(name)


	# Method to fill out the app's bundle ID
	def enter_bundle_identifier(self, bundle_id):
		bundle_id_element = self.driver.find_element_by_name("explicitIdentifier")
		bundle_id_element.send_keys(bundle_id)

	# Method to select the enabled services
	def select_enabled_app_services(self, services):
		for service in services:
			self.driver.find_element_by_name(service).click()

	# Method to click the continue 'button' to move to the confirmation step
	def click_continue_button(self):
		continue_button = self.driver.find_element_by_class_name("submit")
		continue_button.click()

		# Wait until all page content has been added
		time.sleep(0.2)

		# If we've moved onto the next page in the process, there's not been an error
		if "formID=1469461" not in self.driver.current_url:
			# Load the error form elements from the page
			error_elements = self.driver.find_elements_by_class_name("form-error")

			# Are there any error elements?
			if len(error_elements) > 0:

				# Create a list to store the actual errors 
				# (some errors might be in the page but not visible to the user, so they haven't been shown yet)
				errors_list = []

				# Loop through the elements to see which ones are on-screen
				for element in error_elements:

					# The hackiest way to check error visibility
					# Check whether the style of the component is visible
					if "display: none" not in element.get_attribute("style"):

						# If it is visible, append the error message
						errors_list.append(element.get_attribute("innerHTML"))

				# Were there any actual errors?
				if len(errors_list) > 0:
					# Raise an exception with the error codes
					raise Exception(HamperError(1, str(errors_list)))
	
	# Confirm the creation of the app ID
	def click_submit_button(self):
		time.sleep(0.5)

		submit_button = self.driver.find_element_by_css_selector(".button.small.blue.right.submit")
		submit_button.click()