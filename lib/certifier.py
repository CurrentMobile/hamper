#
# GrubyCertifier is the class to handle the creation and downloading of signing certificates
# Instantiate with the cookie jar returned by GrubyAuthenticator and the CSR file path to use. 
# GrubyCertifier will then go off and generate a distribution certificate on the account.
#

import mechanize
import cookielib

class GrubyCertifier(object):
	def __init__(self, cookie_jar, csr_path):
		super(GrubyCertifier, self).__init__()
		self.browser  = mechanize.Browser()
		self.cookie_jar = cookie_jar
		self.csr_path = csr_path

	def generate_certificate(self):
		# Set up the browser options 
		self.browser.set_handle_equiv(True)
		self.browser.set_handle_gzip(True)
		self.browser.set_handle_redirect(True)
		self.browser.set_handle_referer(True)
		self.browser.set_handle_robots(False)

		# This will trigger the provisioning portal to load this page: i.imgur.com/8RmehDm.png
		# It will be prefilled to generate a distribution certificate
		selectCertTypeResponse = self.browser.open("https://developer.apple.com/account/ios/certificate/certificateCreate.action?formID=27276876")

		# Select the certificate type form
		self.browser.select_form("certificateSave")

		# Submit the certificate type form
		response = self.browser.submit()
		print response.read()
		# Select the certificate request form
		# self.browser.select_form(name="certificateRequest")
		# self.browser.submit()


