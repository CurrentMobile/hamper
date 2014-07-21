# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from identifier import HamperIdentifier

from helpers.driver import HamperDriver

class Hamper(object):
	def __init__(self, email, password):
		super(Hamper, self).__init__()

		self.authenticator = HamperAuthenticator(email, password)
		self.certifier = HamperCertifier()
		self.identifier = HamperIdentifier()

h = Hamper(email='', password='')
h.authenticator.sign_in()
h.identifier.generate_app_id("FutureAppTest", "com.mobilexlabs.futureapptest", [HamperIdentifier.HIServicePushNotifications])

# print h.certifier.generate_distribution_certificate("/Users/kiran/Developer/iOS/Signing/CertificateSigningRequest.certSigningRequest")