from google.appengine.ext.db import Model, Key
from google.appengine.api.users import User
import json
import logging
import iso8601
from cgi import escape as htmlEscape
from datetime import datetime

KEY_IDENTIFIER = "id"

def modelListToJson(lst):
	out = []
	for item in lst:
		if isinstance(item, Model):
			out.append(modelToJson(item))
		else:
			out.append(json.dumps(item))
	return "[%s]" % ",".join(out)

def modelToJson(instance):
	tempdict = {}
	for key in instance.properties():
		value = getattr(instance, key)
		tempdict[key] = makeJsonSafe(value)

	tempdict[KEY_IDENTIFIER] = unicode(instance.key())
	jsonString = json.dumps(tempdict)

	return jsonString
	
def jsonToModel(Model, jsonString):
	jsonObj = json.loads(jsonString)
	if jsonObj.has_key(KEY_IDENTIFIER):
		instance = Model.get(jsonObj[KEY_IDENTIFIER])
	else:
		instance = Model()
		
	for property, value in jsonObj.items():
		if hasattr(Model, property):
			value = convertToGaeDatatype(instance, property, value)
			setattr(instance, property, value)
		else:
			if property != KEY_IDENTIFIER:
				logging.info('Ignored the "%s" property not found on the %s class' % (property, Model.__name__))

		
	return instance

def convertToGaeDatatype(instance, property, value):
	if isinstance(getattr(instance,property), datetime):
		return iso8601.parse_date(value)
	elif isinstance(getattr(instance,property), User):
		return User(value)
	elif isinstance(getattr(instance,property), Model):
		return Key(value)
	elif isinstance(getattr(instance,property), str):
		return htmlEscape(value)
	else:
		return value

def makeJsonSafe(value):
	if isinstance(value, Model):
		return unicode(value.key())
	elif isinstance(value, list):
		return [makeJsonSafe(x) for x in value]
	elif isinstance(value, (int, long, float, complex)):
		return value
	elif isinstance(value, bool):
		return value
	elif isinstance(value, datetime):
		return datetime.isoformat(value)
	else:
		return unicode(value)
