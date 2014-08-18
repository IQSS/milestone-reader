#!/bin/sh
echo "Setting up milestone-reader"
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6Server/x86_64/epel-release-6-8.noarch.rpm
yum install -y python-pip python-devel
cd /milestone_reader
pip install -r requirements/local.txt
cd /milestone_reader/milestone_reader/milestone_reader/settings
cp github_api_secrets_template.json github_api_secrets.json 
cd /milestone_reader/milestone_reader
# FIXME: need non-interactive setup
#python manage.py syncdb
echo "Before running, be sure to edit github_api_secrets.json"
