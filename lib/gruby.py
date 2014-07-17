import mechanize

# Import the other modules used in this library
from authenticator import GrubyAuthenticator
from certifier import GrubyCertifier

class Gruby(object):
	def __init__(self, email, password):
		super(Gruby, self).__init__()
		self.email 	  = email
		self.password = password
		self.authenticator = GrubyAuthenticator(email, password)
		self.certifier = GrubyCertifier(self.authenticator.cookie_jar, '/Users/kiran/Developer/iOS/Signing/CertificateSigningRequest.certSigningRequest')

g = Gruby('', '')
cookie_jar = g.authenticator.sign_in()
g.certifier.browser.set_cookiejar(cookie_jar)
g.certifier.generate_certificate()