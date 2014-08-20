#!/bin/sh
source /usr/bin/virtualenvwrapper.sh
WORKON_HOME=~/.virtualenvs
workon milestones
cd /milestone_reader/milestone_reader
# 0.0.0.0 for vagrant port forwarding to work
python manage.py runserver 0.0.0.0:8000 --settings=milestone_reader.settings.local &
