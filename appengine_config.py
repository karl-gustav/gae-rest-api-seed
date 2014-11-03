from google.appengine.api import users

def namespace_manager_default_namespace_for_request():
	# assumes the user is logged in.
	return users.get_current_user().user_id()
