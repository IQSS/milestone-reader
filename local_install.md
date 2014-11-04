## Install (on OS X)

This is a quick checklist to install eyeData on an OS X machine.  Currently, it installs the [twoscoops project template](https://github.com/twoscoops/django-twoscoops-project) for [Django 1.6](https://docs.djangoproject.com/en/1.6/), including creating a database, and running a skeleton site. 

#### Install [pip](http://pip.readthedocs.org/en/latest/installing.html)

* use sudo if needed

#### Install [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

* depends on pip
* remember to set the (shell startup file)[http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file]


#### Pull down the [Milestone Reader repository](https://github.com/IQSS/milestone-reader)

* Use the [mac client](https://mac.github.com/) if desired

#### Setup

##### cd into the eyeData repository

```
cd ~\milestone-reader
```

##### Install the virtualenv and the requirements

This may take a minute or two.  Xcode needs to be installed.
    
```
mkvirtualenv milestones
pip install -r requirements/local.txt
```

If you run into Xcode (or other errors) when running the install, google it.  Sometimes the (Xcode license agreement hasn't been accepted)[http://stackoverflow.com/questions/26197347/agreeing-to-the-xcode-ios-license-requires-admin-privileges-please-re-run-as-r/26197363#26197363]

#### Configure settings (still in ~\milestone_reader)

* Edit the postactivate script for the [virtualenv](http://virtualenv.readthedocs.org/en/latest/)

```
vim $VIRTUAL_ENV/bin/postactivate
```

'vim' may be any text editor

* add these lines to the postactivate file and save the file

```
export DJANGO_DEBUG=True
export DJANGO_SETTINGS_MODULE=milestone_reader.settings.local
```

* Test the 'postactivate' script from the command line

```
deactivate
workon milestones
echo $DJANGO_SETTINGS_MODULE
```

You should see ```milestone_reader.settings.local```

#### Create file with GitHub personal access tokens

1.  Create a file name [```github_api_secrets.json```](https://github.com/IQSS/milestone-reader/blob/master/milestone_reader/milestone_reader/settings/github_api_secrets_template.json) and take proper care of it

```
cd ~/milestone-reader/milestone_reader/milestone_reader/settings
cp github_api_secrets_template.json github_api_secrets.json
```

1. Open the newly created (copied) ```github_api_secrets.json```
1. For each of your repositories, add the name and an appropriate [GitHub Api Token](https://github.com/blog/1509-personal-api-tokens)
   * If you have api read access to several repositories under one organization, you may only need one API token, but it will be repeated for each repository.



#### Install (still in ~\milestone-reader)

```
cd milestone_reader
python manage.py syncdb
```

* Follow the prompts to create a superuser, create tables, etc.



#### Run (still in ~\milestone-reader\milestone_reader)

```
python manage.py runserver
```

* Feel grateful to be alive

#### Add your repositories

1. Navigate to http://127.0.0.1:8000/milestone-reader-admin
1. Enter an organization http://127.0.0.1:8000/milestone-reader-admin/repositories/organization/add/
1. Enter a repository http://127.0.0.1:8000/milestone-reader-admin/repositories/repository/add/

#### Retrieve the milestones

```
cd ~/milestone-reader/milestone_reader/apps/milestones/
python milestone_retriever.py
```

* Example of Milestones listed in the admin
![retrieved milestones](https://github.com/IQSS/milestone-reader/blob/master/milestone_reader/static/images/retrieved_milestones.png)

#### View the milestones (basic template)

* Go to http://127.0.0.1:8000/milestones/by-due-date/

* Example of a basic template:
![open issues list](https://github.com/IQSS/milestone-reader/blob/master/milestone_reader/static/images/open_milestones.png)

* Example of milestones by month, across repos:
![open issues list](https://github.com/IQSS/milestone-reader/blob/master/milestone_reader/static/images/milestones_by_month.png)

#### Edit the files template files

* Location ```~\milestone-reader\milestone_reader\templates```

* ```base.html``` is the over-arching template


## Working with the project (post installation)

```
cd ~\milestone-reader\milestone_reader
workon milestones
python manage.py runserver
```

