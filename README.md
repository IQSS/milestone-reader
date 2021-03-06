milestone-reader
================

Mini project to read/aggregate milestones from several github repositories so that they may be presented on one page.
Live example: (http://roadmap.iq.harvard.edu/)

### Setup

### Initial Install.  

(Assumes [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation))

```
git clone git@github.com:IQSS/milestone-reader.git
cd milestone-reader
mkvirtualenv milestones
pip install -r requirements/local.txt
```

#### Create file with GitHub personal access tokens

1.  Create a file name [```github_api_secrets.json```](https://github.com/IQSS/milestone-reader/blob/master/milestone_reader/milestone_reader/settings/github_api_secrets_template.json) and take proper care of it

```
cd ~/milestone-reader/milestone_reader/milestone_reader/settings
cp github_api_secrets_template.json github_api_secrets.json
```

1. Open the newly created (copied) ```github_api_secrets.json```
1. For each of your repositories, add the name and an appropriate [GitHub Api Token](https://github.com/blog/1509-personal-api-tokens)
   * If you have api read access to several repositories under one organization, you may only need one API token, but it will be repeated for each repository.


#### Create the database and run the server (development mode example)

```
cd milestone_reader
python manage.py syncdb --settings=milestone_reader.settings.local
python manage.py runserver --settings=milestone_reader.settings.local
```

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

### Notes

* Started with [django-twoscoops-project template](https://github.com/twoscoops/django-twoscoops-project)

