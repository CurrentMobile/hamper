# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from identifier import HamperIdentifier
from provisioner import HamperProvisioner

from helpers.driver import HamperDriver
from helpers.date import HamperDate

class Hamper(object):
	def __init__(self):
		super(Hamper, self).__init__()

		self.authenticator = HamperAuthenticator()
		self.certifier = HamperCertifier()
		self.identifier = HamperIdentifier()
		self.provisioner = HamperProvisioner()

h = Hamper()
h.authenticator.sign_in(email='', password='')