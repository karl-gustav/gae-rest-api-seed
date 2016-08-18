import webapp2
from google.appengine.ext import db
from lib.decorators import httpCode_loginRequired
from external_modules.gae_json_model_converter.jsonUtil import modelListToJson
from HTTPExceptions import HTTP400, HTTP403, HTTP404, HTTP415
import logging


def noValidation(object): return True

def generateHandler(Model, createValidator = noValidation, updateValidator = noValidation):
    class GenericHandler(webapp2.RequestHandler):
        @httpCode_loginRequired
        def get(self, key=None):
            gql = self.request.get("filter")
            try:
                if key:
                    self.response.out.write(Model.get(key).toJson())
                else:
                    if gql:
                        instances = Model.gql(gql)
                    else:
                        instances = Model.all()
                    self.response.out.write(modelListToJson(instances))

                self.response.headers['Content-Type'] = 'application/json'
            except KeyError as e:
                raise HTTP404(e)

        @httpCode_loginRequired
        def put(self, key): #update
            if not key:
                raise HTTP404("You can't update an instance if you don't put the identifier in the URL! Use POST for creating!")

            onlyAllowJson(self.request)

            try:
                instance = Model.fromJson(self.request.body)
            except KeyError as e:
                raise HTTP404(e)

            if not instance.is_saved():
                raise HTTP400("You tried to update a object that has no identifier in the object, if this is a new object use POST!")

            if unicode(instance.key()) != key:
                raise HTTP403("JSON identifier in the object don't match the one in the URL!")

            updateValidator(instance)

            instance.put()
            self.response.out.write(instance.toJson())
            self.response.headers['Content-Type'] = 'application/json'

        @httpCode_loginRequired
        def post(self, key=None): # create
            if key:
                raise HTTP404("You can't create a new instance on an existing instance url! Use PUT for updating!")

            onlyAllowJson(self.request)

            instance = Model.fromJson(self.request.body)

            createValidator(instance)

            instance.put()
            self.response.out.write(instance.toJson())
            self.response.headers['Content-Type'] = 'application/json'


        @httpCode_loginRequired
        def delete(self, key):
            if not key:
                raise HTTP404("You need to supply the key you want to delete in the url!")

            try:
                instance = Model.get(key)
            except KeyError as e:
                raise HTTP404(e)

            try:
                instance.delete()
                self.response.out.write('Deleted "%s"!' % instance.key())
            except Exception, e:
                errorMsg = 'There was a problem deleting %s' % key
                logging.error(errorMsg)
                raise Exception(e, errorMsg)

    return GenericHandler

def generateChildHandler(Model, createValidator = noValidation, updateValidator = noValidation):
    class GenericChildHandler(webapp2.RequestHandler):
        @httpCode_loginRequired
        def get(self, parentKey, childKey=None):
            if not existInDB(parentKey):
                raise HTTP404('Could not find the parentKey from the URL in the database')

            try:
                if childKey:
                    self.response.out.write(Model.get(childKey).toJson())
                else:
                    childInstances = Model.allByParentReference(parentKey)
                    self.response.out.write(modelListToJson(childInstances))

                self.response.headers['Content-Type'] = 'application/json'
            except KeyError as e:
                raise HTTP404(e)

        @httpCode_loginRequired
        def put(self, parentKey, childKey): #update
            if not existInDB(parentKey):
                raise HTTP404('Could not find the parentKey from the URL in the database')

            if not childKey:
                raise HTTP404("You can't update an instance if you don't put the identifier in the URL! Use POST for creating!")

            onlyAllowJson(self.request)

            try:
                instance = Model.fromJson(self.request.body)
            except KeyError as e:
                raise HTTP404(e)

            if not instance.is_saved():
                raise HTTP400("You tried to update a object that has no identifier in the object, if this is a new object use POST!")

            if unicode(instance.key()) != childKey:
                raise HTTP403("JSON identifier in the object don't match the one in the URL!")

            updateValidator(instance)

            instance.put()
            self.response.out.write(instance.toJson())
            self.response.headers['Content-Type'] = 'application/json'

        @httpCode_loginRequired
        def post(self, parentKey, childKey=None): # create
            if not existInDB(parentKey):
                raise HTTP404('Could not find the parentKey from the URL in the database')

            if childKey:
                raise HTTP404("You can't create a new instance on an existing instance url! Use PUT for updating!")

            onlyAllowJson(self.request)

            instance = Model.fromJson(self.request.body)
            instance.setParentReference(db.Key(parentKey))

            createValidator(instance)

            instance.put()
            self.response.out.write(instance.toJson())
            self.response.headers['Content-Type'] = 'application/json'


        @httpCode_loginRequired
        def delete(self, parentKey, childKey):
            if not existInDB(parentKey):
                raise HTTP404('Could not find the parentKey from the URL in the database')

            if not childKey:
                raise HTTP404("You need to supply the childKey you want to delete in the url!")

            try:
                instance = Model.get(childKey)
            except KeyError as e:
                raise HTTP404(e)

            try:
                instance.delete()
                self.response.out.write('Deleted "%s"!' % instance.key())
            except Exception, e:
                errorMsg = 'There was a problem deleting %s' % childKey
                logging.error(errorMsg)
                raise Exception(e, errorMsg)

    return GenericChildHandler

def existInDB(keyString):
    return db.Query().filter('__key__ =', db.Key(keyString)).fetch(1) != None

def onlyAllowJson(request):
    if 'application/json' not in request.headers['Content-Type'].lower():
        raise HTTP415('Only Content-Type allowed is application/json!')
