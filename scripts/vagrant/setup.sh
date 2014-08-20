#!/bin/sh
echo "Setting up milestone-reader"
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6Server/x86_64/epel-release-6-8.noarch.rpm
yum install -y python-pip python-devel
pip install virtualenvwrapper
source /usr/bin/virtualenvwrapper.sh
export WORKON_HOME=~/.virtualenvs
mkvirtualenv milestones
workon milestones
cd /milestone_reader
pip install -r requirements/local.txt
cd /milestone_reader/milestone_reader/milestone_reader/settings
cp github_api_secrets_template.json github_api_secrets.json 
cd /milestone_reader/milestone_reader
python manage.py syncdb --settings=milestone_reader.settings.local
# resolve "Site matching query does not exist" and setup root:root
# http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin/23028198#23028198
# http://stackoverflow.com/questions/1466827/automatically-create-an-admin-user-when-running-djangos-manage-py-syncdb
python manage.py loaddata /milestone_reader/scripts/vagrant/fixtures.json --settings=milestone_reader.settings.local
# 0.0.0.0 for vagrant port forwarding to work 
python manage.py runserver 0.0.0.0:8000 --settings=milestone_reader.settings.local &
echo "Before running, be sure to edit github_api_secrets.json"
