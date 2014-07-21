#
# HamperIdentifier is the class to handle the creation of the identifiers used in the provisioning portal
# Use this class to create the app ID for your application.
#

from error import HamperError
from helpers.driver import HamperDriver

from selenium.webdriver.support.ui import WebDriverWait

import time

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
	
	# Confirm the creation of the app ID
	def click_submit_button(self):
		time.sleep(0.5)

		submit_button = self.driver.find_element_by_css_selector(".button.small.blue.right.submit")
		submit_button.click()