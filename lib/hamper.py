# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from error import HamperError

from helpers.driver import HamperDriver

class Hamper(object):
	def __init__(self, email, password):
		super(Hamper, self).__init__()
		self.email 	  = email
		self.password = password

		self.authenticator = HamperAuthenticator(email, password)
		self.certifier = HamperCertifier()

h = Hamper(email='', password='')
h.authenticator.sign_in()
print h.certifier.generate_distribution_certificate("/Users/kiran/Developer/iOS/Signing/CertificateSigningRequest.certSigningRequest")