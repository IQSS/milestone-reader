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
python manage.py validate --settings=milestone_reader.settings.local
python manage.py syncdb --settings=milestone_reader.settings.local
# resolve "Site matching query does not exist" and setup root:root
# http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin/23028198#23028198
# http://stackoverflow.com/questions/1466827/automatically-create-an-admin-user-when-running-djangos-manage-py-syncdb
python manage.py loaddata /milestone_reader/scripts/vagrant/fixtures.json --settings=milestone_reader.settings.local
# resolve "no such column: repositories_repository.is_private" for repository/add/
python manage.py loaddata apps/repositories/fixtures/iqss_initial.json --settings=milestone_reader.settings.local
# Note: `rm -rf /milestone_reader/test_setup` to start over
# python manage.py dumpdata --indent=4 milestones
cp /milestone_reader/milestone_reader/milestone_reader/settings/github_api_secrets.json.local /milestone_reader/milestone_reader/milestone_reader/settings/github_api_secrets.json
python /milestone_reader/milestone_reader/apps/milestones/milestone_retriever.py
# start django
# python /milestone_reader/scripts/vagrant/runserver.sh
# FIXME: why can't we start django programatically from here?
# Should use Apache or nginx anyway, of course. :)
echo "Next steps: vagrant ssh, sudo -i, /milestone_reader/scripts/vagrant/runserver.sh"
