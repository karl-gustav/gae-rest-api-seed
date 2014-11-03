"""
	Helper method to raise exception with 'or':
	somethingBoolean() or raise(HTTP400, 'something bad happended')
"""
def raiseEx(exception, message=''):
	raise exception(message)

"""Generic HTTPCode exception"""
class HTTPCodeException(Exception): pass
	
class HTTP400(HTTPCodeException):
	"""Bad Request"""
	code = 400

class HTTP401(HTTPCodeException):
	"""Unauthorized"""
	code = 401

class HTTP402(HTTPCodeException):
	"""Payment Required"""
	code = 402

class HTTP403(HTTPCodeException):
	"""Forbidden"""
	code = 403

class HTTP404(HTTPCodeException):
	"""Not Found"""
	code = 404

class HTTP405(HTTPCodeException):
	"""Method Not Allowed"""
	code = 405

class HTTP406(HTTPCodeException):
	"""Not Acceptable"""
	code = 406

class HTTP407(HTTPCodeException):
	"""Proxy Authentication Required"""
	code = 407

class HTTP408(HTTPCodeException):
	"""Request Timeout"""
	code = 408

class HTTP409(HTTPCodeException):
	"""Conflict"""
	code = 409

class HTTP410(HTTPCodeException):
	"""Gone"""
	code = 410

class HTTP411(HTTPCodeException):
	"""Length Required"""
	code = 411

class HTTP412(HTTPCodeException):
	"""Precondition Failed"""
	code = 412

class HTTP413(HTTPCodeException):
	"""Request Entity Too Large"""
	code = 413

class HTTP414(HTTPCodeException):
	"""Request-URI Too Long"""
	code = 414

class HTTP415(HTTPCodeException):
	"""Unsupported Media Type"""
	code = 415

class HTTP416(HTTPCodeException):
	"""Requested Range Not Satisfiable"""
	code = 416

class HTTP417(HTTPCodeException):
	"""Expectation Failed"""
	code = 417
