import logging
from google.appengine.api import users
from ..HTTPExceptions import HTTPCodeException, HTTP401

class MissingArgumentException(Exception): pass

def httpCode_loginRequired(func):
	@httpCode
	def _decorator(self, *args, **kwargs):
		if users.get_current_user():
			func(self, *args, **kwargs)
		else:
			raise HTTP401

	return _decorator

def httpCode(func):
	def _decorator(self, *args, **kwargs):
		try:
			func(self, *args, **kwargs)
		except HTTP401, e:
			logging.info("Sending %s because user not logged in!" % e.code)
			self.response.clear()
			self.response.set_status(e.code)
			self.response.headers.add_header("Location", '/Login')
			self.response.out.write("User not logged in! Use the Location header to get the login url.")
		except HTTPCodeException, e:
			logging.info("Catched exception %s! Generating a %s error response!" % (e.__class__.__name__, e.code))
			self.response.clear()
			self.response.set_status(e.code)
			self.response.out.write(e.message)

	return _decorator
