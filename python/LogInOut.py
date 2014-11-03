from google.appengine.ext import webapp
from google.appengine.api.users import create_logout_url, create_login_url

class Login(webapp.RequestHandler):
	def get(self):
		continueUrl = self.request.get('continue') or '/'
		logInUrl = create_login_url(continueUrl)
		self.redirect(logInUrl)

class Logout(webapp.RequestHandler):
	def get(self):
		continueUrl = self.request.get('continue') or '/'
		logOutUrl = create_logout_url(continueUrl)
		self.redirect(logOutUrl)
