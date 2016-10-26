# CZ3003 Crisis Management System

## Running on the cloud

The root url configured is https://crisismanagement.herokuapp.com/

Heroku server is free to use, but it will go to sleep when there is 30 minutes of inactivity. When the next web request goes to the server, it may need 30 secs to load the first time and it will be at normal speeds during subsequent loads.

## Running and Setup

### Install prerequisites

1. Install [Python and Pip](http://install.python-guide.org)

2. Install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref)

3. Install the [Heroku Toolbelt](https://toolbelt.heroku.com/)

4. Install [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)

### First time setup

#### Clone the repo

```sh
$ git clone https://github.com/sngguojie/CZ3003-CMS.git
$ cd CZ3003-CMS
```

#### Create a virtual environment for this repo

```sh
$ virtualenv venv
```

#### Install packages in the virtual environment

```sh
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Setup database and web application assets

```sh
$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic
```

#### Startup the app locally

```sh
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

### Working on the project

[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref) is used to manage package dependecies within the repo.
Before working on the project, the virtual environment *MUST* be enabled:

```sh
$ source venv/bin/activate
```

## Deploying to Heroku

Automatic deployment onto Heroku has already been configured. Just push the changes to Github and the changes will be deployed.

To push the changes:
```sh
$ git add -A;git commit -am 'commit message';git push origin master
```

To check logs:
Go to https://addons-sso.heroku.com/apps/8cd10da0-f859-4fff-8d2e-fd3dccacafa9/addons/1e10afdf-b04b-4dff-9ad6-f63279039ccc 


## Testing

### Running API Tests

1. Get [Postman](https://www.getpostman.com/)

2. In Postman, import the pre-built environment file `localhost` from the `test/postman` folder. This gives a default `url` variable to run tests with.

3. In Postman, import the test collection `ApiTests` in the same folder.

4. Open the Postman Runner in the application, select `ApiTests` and choose the `localhost` environment.

5. Start the server locally and Run the test collection. All tests should pass.


### Creating API Tests

Import the test collection in Postman, and either duplicate the existing tests with modifications, or create new tests. Saving is necessary!


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


## Development Guidelines

Follow the below guidelines when making changes to the project.

### Making Changes

This repository uses a **Rebase -> Pull** Request workflow. The idea is to ensure that most changes are able to be *fast-forwarded* by other members of the team, and to keep the team updated on the same page. In this way, developers fix their own conflicts.

In the workflow, the `master` branch will always be identical to the `master` of the repository, and all changes will be performed on separate branches to be merged after the Pull Requests have been approved.

Follow the steps below when making changes to the project:

#### 1. Perform changes

Perform your changes on a *separate* branch:

```sh
$ git checkout -b add-feature
// Perform changes and Commits
```

#### 2. Rebase your new branch onto the master branch

To ensure that your work can be fast-forwarded onto the master branch (preventing merge conflicts), [rebase](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) your work on the master branch:

```sh
$ git checkout master
$ git pull   // Update master branch
$ git checkout add-feature
$ git rebase master   // Rebase your work onto master
// Fix conflicts here, if any
```

Read the [git rebase](https://git-scm.com/docs/git-rebase) documentation for more options.

#### 3. Push your newly rebased branch

Push your newly rebased branch to a branch on the repository:

```sh
$ git push origin add-feature
```

#### 4. Create a Pull Request

On the repository's page on Github, it should detect your newly created branch and prompt you to create a **Pull Request** for it. 
Alternatively, manually create a Pull Request with your newly pushed branch as a comparison.

Fill up the Pull Request Description following the template provided. Optionally, assign another developer to review your Pull Request.

#### 5. Wait for Approval

In the workflow, new Pull Requests are only merged in after approval by all developers of the repo (or an assigned developer). Developers are to post their approval under the PR comments sections.

Developers can take the opportunity to review the code and suggest optimal changes.

#### 6. Merge the branch

After approval has been given, the creator of the Pull Request is to Merge the pull request with the **Merge** strategy, close the PR, and delete the branch.

