import requests

if __name__=='__main__':
    import os, sys
    from os.path import dirname, abspath, join
    #d1 = dirname(dirname(abspath(__file__)))
    d1 = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(d1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milestone_reader.settings.local")
    
from django.conf import settings

from apps.repositories.models import Organization, Repository
from apps.milestones.models import Milestone

class GitHub_CredentialsException(Exception):
    pass


class MilestoneRetriever:
    """For each visible Repository, retrieve its milestones"""
    
    def __init__(self):
        # Let this blow up on an error
        try:
            self.github_username = settings.GITHUB_REPOSITORY_PASSWORD_DICT['GITHUB_USERNAME']
        except: 
            raise GitHub_CredentialsException("MilestoneRetriever.Failed to retrieve GITHUB_USERNAME from settings")
            
    def retrieve_milstones(self):
        
        for repo in Repository.objects.filter(is_visible=True):
            self.get_repository_milestones(repo)
            break
            
    def get_api_key(self, repo):
        if not type(repo) is Repository:
            raise GitHub_CredentialsException("MilestoneRetriever. Tried to retrieve API key using non-Repository object")
            
        try:
            return settings.GITHUB_REPOSITORY_PASSWORD_DICT['GITHUB_API_ACCESS_TOKENS'][repo.github_name]
        except: 
            raise GitHub_CredentialsException("MilestoneRetriever.Failed to retrieve API key for repository: %s" % repo.github_name)
        
           
    def get_repository_milestones(self, repo):

        milestones_url = repo.get_github_api_url()
        request_auth = (self.github_username, self.get_api_key(repo))
        print 'milestones_url', milestones_url
        req = requests.get(milestones_url, auth=request_auth)

        print (req.status_code)
            
        if not req.status_code == 200:
            # Do something, put this in a db log
            return
        
        try:
            json_response = req.json()
        except:
            # Do something, put this in a db log
            return
            
        print (json_response)
        # update repository information: description, homepage, etc
        # update milestones for repository
       
        
if __name__=='__main__':
    ms = MilestoneRetriever()
    ms.retrieve_milstones()

        
        
        