# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from identifier import HamperIdentifier
from provisioner import HamperProvisioner

from helpers.driver import HamperDriver

class Hamper(object):
	def __init__(self, email, password):
		super(Hamper, self).__init__()

		self.authenticator = HamperAuthenticator(email, password)
		self.certifier = HamperCertifier()
		self.identifier = HamperIdentifier()
		self.provisioner = HamperProvisioner()

h = Hamper(email='', password='')
h.authenticator.sign_in()
h.provisioner.generate_development_profile("com.MobileXLabs.jByhnDyFRPWTaNA", "TestAppppp")	