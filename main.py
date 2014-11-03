import webapp2
from python.RestfulHandler import getHandler
from models import Item
from python.LogInOut import Login, Logout

app = webapp2.WSGIApplication([
		(r'/rest/items/?([^\/\?]+)?', getHandler(Item)),
		(r'/login/?', Login),
		(r'/logout/?', Logout)
	], debug=True)
