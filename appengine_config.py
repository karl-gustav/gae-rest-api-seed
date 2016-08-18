from google.appengine.api import users

def namespace_manager_default_namespace_for_request():
    # Uncomment this line to separate data per user (assumes the user is logged in):
    # return users.get_current_user().user_id()
    pass
