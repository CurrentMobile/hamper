import mechanize

# Import the other modules used in this library
from authenticator import GrubyAuthenticator

class Gruby(object):
	def __init__(self, email, password):
		super(Gruby, self).__init__()
		self.email 	  = email
		self.password = password
		self.authenticator = GrubyAuthenticator(email, password)