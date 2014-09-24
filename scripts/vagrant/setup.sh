#!/bin/sh
echo "Setting up milestone-reader"
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6Server/x86_64/epel-release-6-8.noarch.rpm
yum install -y python-pip python-devel httpd mod_wsgi ack elinks
pip install virtualenvwrapper
source /usr/bin/virtualenvwrapper.sh
mkdir -p /webapps/virtualenvs
export WORKON_HOME=/webapps/virtualenvs
mkvirtualenv milestones
workon milestones
cd /milestone_reader
pip install -r requirements/local.txt
cd /milestone_reader/milestone_reader/milestone_reader/settings
cp github_api_secrets_template.json github_api_secrets.json 
cd /milestone_reader/milestone_reader
python manage.py validate --settings=milestone_reader.settings.production
mkdir -p /webapps/data/milestones
chown apache /webapps/data/milestones
python manage.py syncdb --noinput --settings=milestone_reader.settings.production
# resolve "Site matching query does not exist" and setup root:root
# http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin/23028198#23028198
# http://stackoverflow.com/questions/1466827/automatically-create-an-admin-user-when-running-djangos-manage-py-syncdb
python manage.py loaddata /milestone_reader/scripts/vagrant/fixtures.json --settings=milestone_reader.settings.production
# resolve "no such column: repositories_repository.is_private" for repository/add/
python manage.py loaddata apps/repositories/fixtures/iqss_initial.json --settings=milestone_reader.settings.production
chown apache /webapps/data/milestones/milestones_prod.db3
# Note: `rm -rf /milestone_reader/test_setup` to start over
# python manage.py dumpdata --indent=4 milestones
cp /milestone_reader/milestone_reader/milestone_reader/settings/github_api_secrets.json.local /milestone_reader/milestone_reader/milestone_reader/settings/github_api_secrets.json
# commented out, runserver version
# python /milestone_reader/scripts/vagrant/runserver.sh
#echo "Next steps: vagrant ssh, sudo -i, /milestone_reader/scripts/vagrant/runserver.sh"
echo "Setting up Apache"
mkdir /var/www/milestones
mkdir /var/www/milestones/media # user uploads
mkdir /var/www/milestones/static # images, js, css, etc.
mkdir /var/www/milestones/milestones # wsgi.py
python manage.py collectstatic --noinput --settings=milestone_reader.settings.production
cp /milestone_reader/milestone_reader/milestone_reader/vagrant-centos-wsgi.py /var/www/milestones/milestones/wsgi.py
cp /milestone_reader/deploy/vagrant-centos-milestones.conf /etc/httpd/conf.d/milestones.conf
service httpd start
chkconfig httpd on
# FIXME: put this in cron
python /milestone_reader/milestone_reader/apps/milestones/vagrant-centos-milestone_retriever.py
