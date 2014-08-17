milestone-reader
================

Mini project to read/aggregate milestones from several github repositories so that they may be presented on one page.

### Setup

* Install.  (Assumes virtualenvwrapper)

```
git clone git@github.com:IQSS/milestone-reader.git
cd milestone-reader
mkvirtualenv milestones
pip install -r requirements/local.txt
cd milestone_reader
python manage.py syncdb
python manage.py runserver
```

#### Add your repository

1. Navigate to (http://127.0.0.1:8000/milestone-reader-admin)
1. Enter an organization (127.0.0.1:8000/milestone-reader-admin/repositories/organization/add/)
1. Enter a repository (127.0.0.1:8000/milestone-reader-admin/repositories/repository/add/)



### Notes

* Started with [django-twoscoops-project template](https://github.com/twoscoops/django-twoscoops-project)

