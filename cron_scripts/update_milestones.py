import os, sys
from os.path import dirname, join, abspath
if __name__=='__main__':
    PROJECT_ROOT = dirname(dirname(abspath(__file__)))
    paths = [ join(PROJECT_ROOT, 'milestone_reader')\
            , join(PROJECT_ROOT, 'milestone_reader', 'milestone_reader')\
            , '/home/ubuntu/.virtualenvs/milestones/lib/python2.7/site-packages'\
            ]
    for p in paths:
        sys.path.append(p)
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milestone_reader.settings.production")

from apps.milestones.milestone_retriever import MilestoneRetriever

if __name__=='__main__':
    ms = MilestoneRetriever()
    ms.retrieve_milestones()
    ms.translate_markdown_descriptions_to_html()
    