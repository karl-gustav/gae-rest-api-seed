from google.appengine.ext import db
from python.lib.jsonUtil import modelToJson, jsonToModel
from python.HTTPExceptions import HTTP404

class Parrent(db.Model):
	author = db.UserProperty(auto_current_user_add=True)
	createdDate = db.DateTimeProperty(auto_now_add=True)

	def toJson(self):
		return modelToJson(self)

	@classmethod
	def fromJson(self, json):
		return jsonToModel(self, json)

	@classmethod
	def get(cls, key):
		item = super(Parrent, cls).get(key)
		if not item:
			raiseEx(HTTP404, 'There don\'t exist a %s for the key "%s"!' % (cls.__name__, key))
		return item

"""
One or multiple model objects here!

See here for available types: https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses
"""
class Item(Parrent):
	text = db.StringProperty()
	checked = db.BooleanProperty(default=False)
