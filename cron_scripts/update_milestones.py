import sys

if __name__=='__main__':
    paths = """/home/ubuntu/code/milestone-reader/milestone_reader
/home/ubuntu/code/milestone-reader/milestone_reader/milestone_reader
/home/ubuntu/.virtualenvs/milestones/lib/python2.7/site-packages""".split()
    for p in paths:
        sys.path.append(p)
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milestone_reader.settings.production")

from from apps.milestones.milestone_retriever import MilestoneRetriever

if __name__=='__main__':
    ms = MilestoneRetriever()
    ms.retrieve_milestones()