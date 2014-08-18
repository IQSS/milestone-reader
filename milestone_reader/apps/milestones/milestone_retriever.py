
if __name__=='__main__':
    import os, sys
    from os.path import dirname, abspath, join
    #d2 = dirname(dirname(abspath(__file__)))
    d1 = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(d1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milestone_reader.settings.local")

from datetime import datetime
import requests

from django.conf import settings

from milestone_reader.utils.msg_util import *

from apps.repositories.models import Organization, Repository
from apps.milestones.models import Milestone
from apps.milestones.forms import MilestoneForm


class GitHubCredentialsException(Exception):
    pass

class MilestoneNotSavedException(Exception):
    pass

class MilestoneInvalidException(Exception):
    pass

class MilestoneRetriever:
    """For each visible Repository, retrieve its milestones"""
    
    def __init__(self, delete_removed_milestones=True):

        # Let this blow up on an error
        try:
            self.github_username = settings.GITHUB_REPOSITORY_PASSWORD_DICT['GITHUB_USERNAME']
        except: 
            raise GitHubCredentialsException("MilestoneRetriever.Failed to retrieve GITHUB_USERNAME from settings")

        self.delete_removed_milestones = delete_removed_milestones
        self.retrieval_time = datetime.now()
            
    def retrieve_milestones(self):
        """Iterate through visible repositories and retrieve milestones"""
        
        for repo in Repository.objects.filter(is_visible=True):
            self.get_repository_milestones(repo)
            
            
    def get_api_key(self, repo):
        """Convenience method for retrieving API keys from settings dict: GITHUB_REPOSITORY_PASSWORD_DICT"""
        if not type(repo) is Repository:
            raise TypeError('repo is not a Repository object')
            
        try:
            return settings.GITHUB_REPOSITORY_PASSWORD_DICT['GITHUB_API_ACCESS_TOKENS'][repo.github_name]
        except: 
            raise GitHubCredentialsException("MilestoneRetriever.Failed to retrieve API key for repository: %s" % repo.github_name)
        
           
    def get_repository_milestones(self, repo):
        if not type(repo) is Repository:
            raise TypeError('repo is not a Repository object')
        msgt('Get Milestones for Repository: %s' % repo)
        
        milestones_url = repo.get_github_api_url()
        request_auth = (self.github_username, self.get_api_key(repo))
        print 'milestones_url', milestones_url
        req = requests.get(milestones_url, auth=request_auth)

        msg('Staus code: %s' % req.status_code)

        if not req.status_code == 200:
            # Do something, put this in a db log
            return
        
        try:
            milestone_dict = req.json()
        except:
            # Do something, put this in a db log
            return
        
        github_milestone_ids_for_this_repo = []        # to check later for deletions
        for milestone_dict in milestone_dict:
            github_mstone_id = self.add_update_milestone(repo, milestone_dict)
            if github_mstone_id is not None:
                github_milestone_ids_for_this_repo.append(github_mstone_id)

        self.delete_milestones_no_longer_in_github(repo, github_milestone_ids_for_this_repo)
        
    def delete_milestones_no_longer_in_github(self, repo, github_ids_to_exclude_for_repo):
        if not type(repo) is Repository:
            raise TypeError('repo is not a Repository object')

        if not type(github_ids_to_exclude_for_repo) is list:
            raise TypeError('milestone_dict is not a list object')
            
        if not self.delete_removed_milestones:
            return 
          
        dashes() 
        msg('Delete local milestones that were erased from github')
        
        milestones_to_delete = Milestone.objects.filter(repository=repo).exclude(github_id__in=github_ids_to_exclude_for_repo)
        
        num_to_delete = milestones_to_delete.count()
        
        if num_to_delete > 0:
            msg('-- Preparing to delete %s removed milestones' % num_to_delete)
            milestones_to_delete.delete()
            msg('-- Milestones deleted')
        else:
            msg('-- No milestones to delete')
     
    def add_update_milestone(self, repo, milestone_dict):
        """
        Update the milestones for single repository
        """        
        if not type(repo) is Repository:
            raise TypeError('repo is not a Repository object')

        if not type(milestone_dict) is dict:
            raise TypeError('milestone_dict is not a dict object')
            
        #msg('add_update_milestone')

        # This is temporarily removed for form evaluation
        github_id = milestone_dict.get('id', None)
        
        # Add two attributes to the API returned dict
        milestone_dict['last_retrieval_time'] = self.retrieval_time
        milestone_dict['repository'] = repo.id
        
        # Format a subset dict for form evaluation
        mstone_params = MilestoneForm.prepare_github_api_resp_for_validation(milestone_dict )

        # Prepare to evaluate the form
        mform = MilestoneForm(mstone_params)
        if mform.is_valid():
            # valid params 
            valid_milestone_params = mform.cleaned_data
                        
            # Does this milestone exist?
            milestone_to_update, created = Milestone.objects.get_or_create(github_id=github_id, defaults=valid_milestone_params)
            
            if created: 
               pass
               msg('created. milestone_to_update: %s' % ( milestone_to_update))
            else:
                # Update the values
                for attr, value in valid_milestone_params.items(): 
                    setattr(milestone_to_update, attr, value)
                milestone_to_update.save()
                msg('updated. milestone_to_update: %s' % (milestone_to_update))
            
            return milestone_to_update.github_id
                
        else:
            raise MilestoneInvalidException('Milestone data did not pass form validation')

            
         
    def update_repository(self, repo, json_response):
        if repo is None or json_response is None:
            return False
        
        # to do     
            
        return False
            
if __name__=='__main__':
    ms = MilestoneRetriever()
    ms.retrieve_milestones()
    
    #repo = Repository.objects.get(pk=2)
    #milestone_dict = MilestoneForm.get_test_milestone()
    #ms = MilestoneRetriever()
    #ms.update_milestone(repo, milestone_dict)
    
        
        
        