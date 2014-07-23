#
# HamperError is the class to handle the errors returned from this library
#

class HamperError(object):
	HECodeDisabledCertificateType = -1
	HECodeInvalidAppID			  = -2
	HECodeInvalidCertificateExpirationDate = -3
	HECodeLogInError = -4

	def __init__(self, code, message):
		super(HamperError, self).__init__()
		self.code 	 = code
		self.message = message

