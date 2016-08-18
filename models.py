from google.appengine.ext import db
from python.external_modules.gae_json_model_converter.jsonUtil import modelToJson, jsonToModel

class Parent(db.Model):
    author = db.UserProperty(auto_current_user_add=True)
    createdDate = db.DateTimeProperty(auto_now_add=True)

    def toJson(self):
        return modelToJson(self)

    @classmethod
    def fromJson(cls, json):
        return jsonToModel(cls, json)

    @classmethod
    def get(cls, key):
        item = super(Parent, cls).get(key)
        if not item:
            raise KeyError('There don\'t exist a %s for the key "%s"!' % (cls.__name__, key))
        return item

    def setParentReference(self, instanceOrKey):
        """Abstract method for setting parent reference"""
        raise Exception('Needs to be overridden in child classes')

    @classmethod
    def allByParentReference(cls, parentKey):
        """Abstract method for getting all instances by parent key"""
        raise Exception('Needs to be overridden in child classes')

"""
One or multiple model objects here!

See here for available types: https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses
"""
class Item(Parent):
    text = db.StringProperty()
    checked = db.BooleanProperty(default=False)

    # Parent is responsible for deleting child objects on delete
    def delete(self):
        db.delete(self.subItems)
        return super(Item, self).delete()


class SubItem(Parent):
    text = db.StringProperty()
    item = db.ReferenceProperty(Item, collection_name='subItems')

    def setParentReference(self, instanceOrKey):
        self.item = instanceOrKey

    @classmethod
    def allByParentReference(cls, parentKey):
        return super(SubItem, cls).all().filter('item =', Item.get(parentKey))

    # Parent is responsible for deleting child objects on delete
    def delete(self):
        db.delete(self.subSubItems)
        return super(SubItem, self).delete()

class SubSubItem(Parent):
    text = db.StringProperty()
    subItem = db.ReferenceProperty(SubItem, collection_name='subSubItems')

    def setParentReference(self, instanceOrKey):
        self.subItem = instanceOrKey

    @classmethod
    def allByParentReference(cls, parentKey):
        return super(SubSubItem, cls).all().filter('subItem =', SubItem.get(parentKey))

