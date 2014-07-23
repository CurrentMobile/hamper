#!/usr/local/bin/python

"""

Hamper

Usage:
  hamper.py auth login --email=<email> --password=<password>
  hamper.py cert create --type=<cert_type> --csr_path=<csr_path> [--app_id=<app_id>]
  hamper.py identifier create --app_name=<app_name> --bundle_id=<bundle_id> [--enabled_services=<app_service>...]
  hamper.py profile create --name=<profile_name> --bundle_id=<bundle_id> --type=<profile_type> [(--exp_day=<exp_day> --exp_month=<exp_month> --exp_year=<exp_year>)]

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

class Hamper(object):
	def __init__(self):
		super(Hamper, self).__init__()

		self.authenticator = HamperAuthenticator()
		self.certifier 	   = HamperCertifier()
		self.identifier    = HamperIdentifier()
		self.provisioner   = HamperProvisioner()

h = Hamper()

def handle_auth_action(arguments):
	try:
		h.authenticator.sign_in(email=arguments['--email'], password=arguments['--password'])
		print colored("User successfully authenticated.", "green")
	except Exception, e:
		if len(e.args) > 0 and hasattr(e.args[0], 'message'):
			print colored(e.args[0].message, "red")
		else:
			print colored(e, "red")
		

def handle_cert_action(arguments):
	pass
	
def handle_identifier_action(arguments):
	pass

def handle_profile_action(arguments):
	pass

def parse_arguments(arguments):
	if arguments['auth'] == True:
		handle_auth_action(arguments)	
	elif arguments['cert'] == True:
		handle_cert_action(arguments)
	elif arguments['identifier'] == True:
		handle_identifier_action(arguments)
	elif arguments['profile'] == True:
		handle_profile_action(arguments)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Hamper 0.1')
    parse_arguments(arguments)