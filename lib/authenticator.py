#
# GrubyAuthenticator is the class to handle the authentication part of the provisioning portal.
# Instantiate with the email and password you want, it'll pass back the cookie jar if successful,
# or an error message on failure
#

import mechanize
import cookielib

class GrubyAuthenticator(object):

	def __init__(self, email, password):
		super(GrubyAuthenticator, self).__init__()
		self.email 	  = email
		self.password = password
		self.browser  = mechanize.Browser()
		self.cookie_jar = cookielib.LWPCookieJar()
		self.browser.set_cookiejar(self.cookie_jar)

	def sign_in(self):

		# Set up the browser options 
		self.browser.set_handle_equiv(True)
		self.browser.set_handle_gzip(True)
		self.browser.set_handle_redirect(True)
		self.browser.set_handle_referer(True)
		self.browser.set_handle_robots(False)

		# Open the profile URL. This will forward to the sign in page if session is invalid
		response = self.browser.open("https://developer.apple.com/account/ios/profile/")

		# Select the first form
		self.browser.select_form(nr=0)

		# Set the email and password fields on that form
		self.browser.form["appleId"] = self.email
		self.browser.form["accountPassword"] = self.password

		# Submit the form
		self.browser.submit()

		# Return the cookie jar object
		return self.browser._ua_handlers['_cookies'].cookiejar
