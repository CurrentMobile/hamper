#!/usr/bin/env python

"""

Hamper

Usage:
  hamper.py auth login --email=<email> --password=<password>
  hamper.py cert create (development | development_push | distribution | distribution_push) --csr_path=<csr_path> --cert_path=<cert_path> [--bundle_id=<bundle_id>]
  hamper.py identifier create --app_name=<app_name> --bundle_id=<bundle_id> [--enabled_services=<app_service>...]
  hamper.py profile create (development | app_store | ad_hoc) --name=<profile_name> --bundle_id=<bundle_id> --profile_path=<profile_path> [(--exp_day=<exp_day> --exp_month=<exp_month> --exp_year=<exp_year>)]

"""

# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from identifier import HamperIdentifier
from provisioner import HamperProvisioner

from helpers.driver import HamperDriver
from helpers.date import HamperDate
from helpers.error import HamperError

# Used for building the CLI
from docopt import docopt
from termcolor import colored

# Used for access the computer's keychain (for storing login credentials)
import keyring

# Used to determine the file's current path (not directory of user when exec'ing via Terminal)
import inspect, os

# Create the class for holding all the Hamper instances
class Hamper(object):
	def __init__(self):
		super(Hamper, self).__init__()

		self.authenticator = HamperAuthenticator()
		self.certifier 	   = HamperCertifier()
		self.identifier    = HamperIdentifier()
		self.provisioner   = HamperProvisioner()

# Instantiate this thing
h = Hamper()

# Helper method to save the login details
def save_login_details(email, password):

	# Save the username and password to the keychain
	keyring.set_password("hamper", email, password)

	# Store the current email address being used to a text file.
	# This allows us to maintain a persistent 'session'.
	# When the user tries to execute a Hamper action (create a certificate, for example), Hamper will find the 
	# cached email address stored in the 'session' file, then fetch the corresponding password from the keychain.
	# Then, Hamper will run the HamperAuthenticator method with these credentials to sign the user in and create the WebDriver session.

	home_directory = os.path.expanduser("~")

	with open(home_directory + "/.hamper_session", "w+") as content_file:
		content_file.write(email)

# Helper method to fetch the cached login details
def cached_login_details():
	home_directory = os.path.expanduser("~")

	# Get the currently-auth'd email address
	with open(home_directory + "/.hamper_session", 'r') as content_file:
		content = content_file.read()

		# Grab the login credentials from the keychain
		return content, keyring.get_password("hamper", content)

# ----
# Methods to handle the CLI actions
# ----


#
# Called when the user tries 'hamper auth ...' 
# Handles the login actions
#
def handle_auth_action(arguments):
	# Sign in with the provided credentials
	h.authenticator.sign_in(email=arguments['--email'], password=arguments['--password'])

	# If the sign in was successful, save the credentials to the keychain and session file
	save_login_details(arguments['--email'], arguments['--password'])
		
#
# Called when the user tries 'hamper cert ...'
# Handles the generation of certificates
#
def handle_cert_action(arguments):

	# Fetch the cached username and password
	cached_email, cached_password = cached_login_details()

	# Start the user's session
	h.authenticator.sign_in(email=cached_email, password=cached_password)

	# Find which certificate the user is requesting, generate accordingly
	if arguments['development']:
		h.certifier.generate_development_certificate(arguments['--csr_path'], arguments['--cert_path'])

	elif arguments['development_push']:
		h.certifier.generate_development_push_certificate(arguments['--bundle_id'], arguments['--csr_path'], arguments['--cert_path'])

	elif arguments['distribution']:
		h.certifier.generate_distribution_certificate(arguments['--csr_path'], arguments['--cert_path'])

	elif arguments['distribution_push']:
		h.certifier.generate_distribution_push_certificate(arguments['--bundle_id'], arguments['--csr_path'], arguments['--cert_path'])

#
# Called when the user tries 'hamper identifier ...'
# Handles the generation of the app IDs
#
def handle_identifier_action(arguments):	

	# Create empty list to hold the translated enabled services
	enabled_services_list = []

	# Loop though each enabled service, adding the translated value to the list
	for service in arguments['--enabled_services']:
		if service == "app_groups":
			enabled_services_list.append(HamperIdentifier.HIServiceAppGroups)
		elif service == "associated_domains":
			enabled_services_list.append(HamperIdentifier.HIServiceAssociatedDomains)
		elif service == "data_protection":
			enabled_services_list.append(HamperIdentifier.HIServiceDataProtection)
		elif service == "health_kit":
			enabled_services_list.append(HamperIdentifier.HIServiceHealthKit)
		elif service == "home_kit":
			enabled_services_list.append(HamperIdentifier.HIServiceHomeKit)
		elif service == "wireless_accessory_config":
			enabled_services_list.append(HamperIdentifier.HIServiceWirelessAccessory)
		elif service == "icloud":
			enabled_services_list.append(HamperIdentifier.HIServiceiCloud)
		elif service == "inter_app_audio":
			enabled_services_list.append(HamperIdentifier.HIServiceInterAppAudio)
		elif service == "passbook":
			enabled_services_list.append(HamperIdentifier.HIServicePassbook)
		elif service == "push":
			enabled_services_list.append(HamperIdentifier.HIServicePushNotifications)
		elif service == "vpn_config":
			enabled_services_list.append(HamperIdentifier.HIServiceVPNConfiguration)
	
	# Fetch the cached username and password
	cached_email, cached_password = cached_login_details()

	# Start the user's session
	h.authenticator.sign_in(email=cached_email, password=cached_password)

	# Generate the app ID with the provided details
	h.identifier.generate_app_id(arguments['--app_name'], arguments['--bundle_id'], enabled_services_list)

#
# Called when the user tries 'hamper profile ...'
# Handles the creation of provisioning profiles
#
def handle_profile_action(arguments):
	# Fetch the cached username and password
	cached_email, cached_password = cached_login_details()

	# Start the user's session
	h.authenticator.sign_in(email=cached_email, password=cached_password)

	# Figure out whether the user is requesting a development, App Store, or AdHoc provisioning profile
	if arguments['development']:

		# Generate the development provisioning profile
		h.provisioner.generate_development_profile(arguments['--bundle_id'], arguments['--name'], arguments['--profile_path'])
	elif arguments['app_store']:

		# Parse out the expiration date of the certificate to use when creating the provisioning profile
		date = HamperDate(month=arguments['--exp_month'], day=arguments['--exp_day'], year=arguments['--exp_year'])

		# Generate the App Store provisioning profile
		h.provisioner.generate_app_store_profile(arguments['--bundle_id'], arguments['--name'], profile_path, date)
	elif arguments['ad_hoc']:
		# Parse out the expiration date of the certificate to use when creating the provisioning profile
		date = HamperDate(month=arguments['--exp_month'], day=arguments['--exp_day'], year=arguments['--exp_year'])

		# Generate the AdHoc provisioning profile
		h.provisioner.generate_adhoc_profile(arguments['--bundle_id'], arguments['--name'], profile_path, date)

#
# Parent method to parse out the required action, and call the appropriate method
#
def parse_arguments(arguments):
	# Wrap in a try-catch so we can print a pretty error message to the console if necessary
	try:
		# Find the action being requested
		if arguments['auth'] == True:
			handle_auth_action(arguments)	
		elif arguments['cert'] == True:
			handle_cert_action(arguments)
		elif arguments['identifier'] == True:
			handle_identifier_action(arguments)
		elif arguments['profile'] == True:
			handle_profile_action(arguments)
	except Exception, e:

		# If there is a HamperError instance being passed as an argument,
		# grab the error message of that and print that to the console.
		if len(e.args) > 0 and hasattr(e.args[0], 'message'):
			print colored("ERROR: " + e.args[0].message, "red")
		else:
			print colored(e, "red")

def pack():
    arguments = docopt(__doc__, version='Hamper 0.1.5')
    parse_arguments(arguments)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Hamper 0.1.5')
    parse_arguments(arguments)