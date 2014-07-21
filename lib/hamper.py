import mechanize

# Import the other modules used in this library
from authenticator import HamperAuthenticator
from certifier import HamperCertifier
from error import HamperError

from selenium import webdriver
import inspect

class Hamper(object):
	def __init__(self, email, password):
		super(Hamper, self).__init__()
		self.email 	  = email
		self.password = password
		self.driver	  = webdriver.Chrome()

		self.authenticator = HamperAuthenticator(email, password)
		self.certifier = HamperCertifier('/Users/kiran/Developer/iOS/Signing/CertificateSigningRequest.certSigningRequest')

h = Hamper('', '')
h.authenticator.sign_in(h.driver)
h.certifier.generate_certificate(h.driver, HamperCertifier.HCCertificateTypeDevelopmentPush)