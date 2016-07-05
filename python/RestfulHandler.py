import webapp2
from lib.decorators import httpCode_loginRequired
from external_modules.gae_json_model_converter.jsonUtil import modelListToJson
from HTTPExceptions import HTTP400, HTTP403, HTTP404, HTTP415
import logging


def noValidation(object): return True

def getHandler(Model, createValidator = noValidation, updateValidator = noValidation):
    class GenericHandler(webapp2.RequestHandler):
        @httpCode_loginRequired
        def get(self, key=None):
            if key:
                self.response.out.write(Model.get(key).toJson())
            else:
                models = Model.all()
                self.response.out.write(modelListToJson(models))

            self.response.headers['Content-Type'] = 'application/json'

        @httpCode_loginRequired
        def put(self, key): #update
            if not key:
                raise HTTP404("You can't update an instance if you don't put the identifier in the URL! Use POST for creating!")
            onlyAllowJson(self.request)
            instance = Model.fromJson(self.request.body)

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

            model = Model.get(key)

            try:
                model.delete()
                self.response.out.write('Deleted "%s"!' % model.key())
            except Exception, e:
                errorMsg = 'There was a problem deleting %s' % key
                logging.error(errorMsg)
                raise Exception(e, errorMsg)

    return GenericHandler


def onlyAllowJson(request):
    if 'application/json' not in request.headers['Content-Type'].lower():
        raise HTTP415('Only Content-Type allowed is application/json!')
