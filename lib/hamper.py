import mechanize

# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier

class Hamper(object):
	def __init__(self, email, password):
		super(Hamper, self).__init__()
		self.email 	  = email
		self.password = password
		self.authenticator = HamperAuthenticator(email, password)
		self.certifier = HamperCertifier(self.authenticator.cookie_jar, '/Users/kiran/Developer/iOS/Signing/CertificateSigningRequest.certSigningRequest')

h = Hamper('', '')
cookie_jar = h.authenticator.sign_in()
