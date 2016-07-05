## Intro:

This repo was made so that new users to Google App Engine should be able
to create a frontend heavy app with a REST api with the least possible
effort.


### Initial setup/installation:
1. Install dependencies with `git submodule init` and `git submodule update`

### How to get started:

1. Download and install the Google App Engine SDK https://cloud.google.com/appengine/downloads
2. Get a new Google App Engine application at http://appengine.google.com
3. Insert the application ID you got in the previous step inn the top of the `app.yaml` file
4. Run your application locally with this command: `dev_appserver.py .`
5. Upload your application with this command: `appcfg.py update .`


### How to create the frontend code:

1. Add/Edit files inside the html folder


### How to create your own models for the REST api:

1. Add your models in the `python/models.py` file, there is a Item model
   that you can use as a starting point
2. Import your new models into the `main.py` file and choose the urls
   you want for your API. Use the Item urls as a starting point


### How to upload different versions:

1. Change the `version:` line in the `app.yaml` file
2. Access your new version directly by going to
   `http://<your version>.<your app id>.appspot.com/`
   (all versions you have are available like this)
3. Set this new version as the default version being served at
   `http://<your app id>.appspot.com/` by selecting it as 
   the default version in the application dashboard at
   http://appengine.google.com (the first version you uploaded is 
   the default one if you don't change it)


### How to make all users share the same data:

1. Delete the `appengine_config.py` file. This file namespace the data
   so all users by all intensive purposes have separate "databases"


### How to remove the Google login:

1. Delete the `appengine_config.py` file
2. Change the `@httpCode_loginRequired` decorator in
   `python/RestfulHandler.py` to `@httpCode`
3. Remove the `login: required` line in `app.yaml` file

### How to minify the frontend code:

1. Install npm (node) http://nodejs.org/
2. Run the command `npm install` to get the required dependencies
3. Run the command `npm build` to generate the `dist/` folder that
   contains your production ready code.
4. Upload your production code to Google App Engine with the command
   `appcfg.py update dist/`
5. Repeat step 3 every time your want to generate the production code
   (every time you have made changes)
