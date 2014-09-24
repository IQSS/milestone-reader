
if __name__=='__main__':
    import os, sys
    from os.path import dirname, abspath, join
    #d2 = dirname(dirname(abspath(__file__)))
    d1 = dirname(dirname(dirname(abspath(__file__))))
    sys.path.append(d1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milestone_reader.settings.production")

from datetime import datetime
import requests
import json
from django.conf import settings
from django.core.mail import send_mail

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
    
    def __init__(self, delete_removed_milestones=True, **kwargs):

        # Let this blow up on an error
        try:
            self.github_username = settings.GITHUB_REPOSITORY_PASSWORD_DICT['GITHUB_USERNAME']
        except: 
            raise GitHubCredentialsException("MilestoneRetriever.Failed to retrieve GITHUB_USERNAME from settings")
            
        self.update_repo_description = kwargs.get('update_repo_description', True)
        self.delete_removed_milestones = delete_removed_milestones
        self.retrieval_time = datetime.now()
    
    
    def send_admin_error_email(self, err_msg):
        
        try:
            admin_email = settings.ADMINS[0][0]
        except:
            return
    

        send_mail('Milestone update failed'\
                , err_msg\
                , admin_email\
                , [admin_email]\
                , fail_silently=False\
                )
    
    
    def update_repository_info(self):
    
        repos = Repository.objects.select_related(\
                                'parent_repository', 
                            ).filter(is_visible=True)
    
        for repo in repos:
            self.update_single_repository(repo)
    
    def format_failed_response_err_msg(self, description, repo, request_url, resp_obj):
        if not type(description) is str:
            raise TypeError('description not a str')
        if not type(request_url) is str:
            raise TypeError('request_url not a str')
        if resp_obj is None:
            raise TypeError('resp_obj is None')
        
        return """%s\

---------------
repository/milestone: %s
---------------
url: %s
---------------
status code: %s
---------------
response: 
%s
---------------
""" % (description, repo, request_url, resp_obj.status_code, resp_obj.text )
        
        
        
    
    def update_single_repository(self, repo):
        """
        Retrieve repository information via the github api.
        Update the repository description, etc.
        
        example of api url: https://api.github.com/repos/IQSS/dataverse
        """
        if not type(repo) == Repository:
            return False
        msgt('Repository update: %s' % repo)
         
        repo_api_url = repo.get_github_api_url()
        request_auth = (self.github_username, self.get_api_key(repo))
    
        msg('repo_api_url: %s' % repo_api_url)
        r = requests.get(repo_api_url, auth=request_auth)

        msg('Staus code: %s' % r.status_code)

        if not r.status_code == 200:
            err_msg = self.format_failed_response_err_msg(\
                                'Bad status code. Update of repository description failed'\
                                , repo
                                , repo_api_url
                                , r)
            self.send_admin_error_email(err_msg)
            return False

        try:
            repo_dict = r.json()
        except:
            err_msg = self.format_failed_response_err_msg(\
                                'r.json() failed. Update of repository description failed'\
                                , repo
                                , repo_api_url
                                , r)
            self.send_admin_error_email(err_msg)
            return False
            
        # { github attribute : Repository object attribute }
        attributes_to_update = dict(description='description'\
                                    , homepage='homepage'\
                                    , private='is_private'
                                    , id='github_id')

        msg(attributes_to_update)
        for github_key, repo_key in attributes_to_update.items():
            if repo_dict.has_key(github_key):
                val = repo_dict.get(github_key, '')
                if val is None:
                    val = ''
                repo.__dict__[repo_key] = val

        repo.save()
        return True
    
    def translate_markdown_descriptions_to_html(self):
        """Use GitHub's markdown API to translate markdown to html
        {
          "text": "Hello world github/linguist#1 **cool**, and #1!",
          "mode": "gfm",
          "context": "github/gollum"
        }
        """
        markdown_url = 'https://api.github.com/markdown'
        mstones = Milestone.objects.select_related(\
                            'repository', 'repository__organization'\
                            ).filter(repository__is_visible=True)
        for ms in mstones:
            msgt('get markdown for ms: %s' % ms.id)
            request_auth = (self.github_username, self.get_api_key(ms.repository))
            context_str = "%s/%s" % (ms.repository.organization.github_login, ms.repository.github_name)
            payload = { "text" : ms.description\
                        , "mode" : "gfm"\
                        , "context" : context_str
            }
            print payload
            r = requests.post(markdown_url, auth=request_auth, data=json.dumps(payload))

            if r.status_code == 200:
                print r.text
                ms.markdown_description = r.text
                ms.save()
                continue
            
            err_msg = self.format_failed_response_err_msg(\
                                'Failed: translate_markdown_descriptions_to_html'\
                                , ms
                                , markdown_url
                                , r)
            self.send_admin_error_email(err_msg)
        
          
    
    def retrieve_milestones(self):
        """Iterate through visible repositories and retrieve milestones"""
        
        for repo in Repository.objects.filter(is_visible=True):
            self.get_repository_milestones(repo)
            repo.last_retrieval_time = self.retrieval_time
            repo.save()
            
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
        
        milestones_url = repo.get_github_api_url(milestones=True)
        request_auth = (self.github_username, self.get_api_key(repo))
        print 'milestones_url', milestones_url
        req = requests.get(milestones_url, auth=request_auth)

        msg('Staus code: %s' % req.status_code)

        if not req.status_code == 200:
            err_msg = self.format_failed_response_err_msg(\
                        'Bad status code. Failed: get_repository_milestones'\
                        , repo
                        , milestones_url
                        , req)
            self.send_admin_error_email(err_msg)
            return
        
        try:
            milestone_dict = req.json()
        except:
            err_msg = self.format_failed_response_err_msg(\
                        ' req.json() Failed: get_repository_milestones'\
                        , repo
                        , milestones_url
                        , req)
            self.send_admin_error_email(err_msg)
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
            # valid params from the form
            valid_milestone_params = mform.cleaned_data
            
            # set the markdown_description field as blank
            valid_milestone_params['markdown_description'] = ''

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

            
        
            
if __name__=='__main__':
    ms = MilestoneRetriever()
    ms.update_repository_info()
    ms.retrieve_milestones()
    ms.translate_markdown_descriptions_to_html()
    
    #repo = Repository.objects.get(pk=2)
    #milestone_dict = MilestoneForm.get_test_milestone()
    #ms = MilestoneRetriever()
    #ms.update_milestone(repo, milestone_dict)
    
        
        
        
