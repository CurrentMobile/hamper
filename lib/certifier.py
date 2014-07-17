#
# GrubyCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by GrubyAuthenticator and the CSR file path to use. 
# GrubyCertifier will then go off and generate a distribution certificate on the account.
#

import mechanize
import cookielib

class GrubyCertifier(object):
	def __init__(self, cookie_jar, csr_path):
		super(certifier, self).__init__()
		self.email 	  = email
		self.password = password
		self.browser  = mechanize.Browser()
		self.browser.set_cookiejar(selfcookie_jar)
		
	def generate_certificate():
		
		pass