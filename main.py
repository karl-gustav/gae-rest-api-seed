import webapp2
from python.RestfulHandler import generateHandler, generateChildHandler
from models import Item, SubItem, SubSubItem
from python.LogInOut import Login, Logout

app = webapp2.WSGIApplication([
    (r'/rest/items/?([^\/\?]+)?', generateHandler(Item)),
    (r'/rest/items/([^\/\?]+)/subitems/?([^\/\?]+)?', generateChildHandler(SubItem)),
    (r'/rest/items/[^\/\?]+/subitems/([^\/\?]+)/subsubitems/?([^\/\?]+)?', generateChildHandler(SubSubItem)), #only need last two keys
    (r'/login/?', Login),
    (r'/logout/?', Logout)
], debug=True)
