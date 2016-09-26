# CZ3003 Crisis Management System

## Running on the cloud

The root url configured is https://cz3003cms.herokuapp.com/

Heroku server is free to use, but it will go to sleep when there is 30 minutes of inactivity. When the next web request goes to the server, it may need 30 secs to load the first time and it will be at normal speeds during subsequent loads.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/sngguojie/CZ3003-CMS.git
$ cd CZ3003-CMS

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

Automatic deployment onto Heroku has already been configured. Just push the changes to Github and the changes will be deployed.

To push the changes:
```sh
$ git add -A;git commit -am 'commit message';git push origin master
```

To check logs:
Go to https://addons-sso.heroku.com/apps/8cd10da0-f859-4fff-8d2e-fd3dccacafa9/addons/1e10afdf-b04b-4dff-9ad6-f63279039ccc 

## To create a new entity
```sh
$ python manage.py startapp <entity_name>
```
A new folder named <entity_name> will be created with the associated files inside and already linked to existing files

To write the attributes for the model, follow conventions and reference at https://docs.djangoproject.com/en/1.10/topics/db/models/

To write views (the processes that a HTTP request will trigger): https://docs.djangoproject.com/en/1.10/topics/http/views/

To make queries (CRUDL) to the database, follow https://docs.djangoproject.com/en/1.10/topics/db/queries/

To map the URL to the correct view/function: Add the url into "CZ3003CMS/urls.py"
Reference: https://docs.djangoproject.com/en/1.10/topics/http/urls/


Once done with the entity, write documentation on what is the URL and the returning JSON format Below: