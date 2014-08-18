import json
from datetime import datetime

from django.forms import ModelForm

from apps.milestones.models import Milestone, GITHUB_TIME_FORMAT_STRING

API_TO_MODEL_KEY_DICT = { 'is_open' : 'state'\
                        , 'github_id' : 'id'\
                        , 'github_number' : 'number'\
                        }

class MilestoneFormNoRepositoryException(Exception):
    pass

# "2014-08-15T18:18:04Z"
#datetime.strptime('2014-08-15T18:18:04Z', GITHUB_TIME_FORMAT_STRING)


class MilestoneForm(ModelForm):

    class Meta:
        model = Milestone
        fields = [ 'repository'\
                , 'title', 'description'\
                , 'open_issues', 'closed_issues'\
                #, 'is_open', 'github_id', 'github_number' # name differs github vs. Milestone object
                , 'is_open', 'github_number' # name differs github vs. Milestone object
                , 'updated_at', 'due_on'\
                , 'last_retrieval_time'\
                ]

    @staticmethod
    def prepare_github_api_resp_for_validation(api_dict):
        """
        - Take the milestone dict returned from the GitHub API
        - Format a separate dict only for form evaluation
            - Temporarily remove the Milestone.github_id / or "id" in the API response
                - Form won't evaluate as 'is_valid()' with a duplicate github_id
        """
            
        if not type(api_dict) == dict:
            raise TypeError('"api_dict" is not a dict') 

        #for k, v in api_dict.items():
        #    print(k, v)
        fmt_dict = {}
        for field_name in MilestoneForm._meta.fields:
            api_key_name = API_TO_MODEL_KEY_DICT.get(field_name, field_name)
            val = api_dict.get(api_key_name, None)
            if api_key_name == 'state':    # Handle the 'is_open' field
                if val == 'open':
                    val = True
                else:
                    val = False
            elif api_key_name in ('updated_at', 'due_on') and not val in (None, ''):    
                try:
                    val = datetime.strptime(val, GITHUB_TIME_FORMAT_STRING)
                except:
                    val= None
            
            fmt_dict[field_name] = val
        #for k, v in fmt_dict.items():
        #    print(k, v)    
               
        return fmt_dict 
        
    @staticmethod
    def get_test_milestone():
        return json.loads('''{
    "url": "https://api.github.com/repos/IQSS/dataverse/milestones/2",
    "labels_url": "https://api.github.com/repos/IQSS/dataverse/milestones/2/labels",
    "id": 715294,
    "number": 2,
    "title": "Beta 1 - Dataverse 4.0",
    "description": "http://datascience.iq.harvard.edu/blog/dataset-versioning-dataverse-40-beta",
    "creator": {
      "login": "eaquigley",
      "id": 5922904,
      "avatar_url": "https://avatars.githubusercontent.com/u/5922904?v=2",
      "gravatar_id": "f47faf108157e51232d48097a2d9790f",
      "url": "https://api.github.com/users/eaquigley",
      "html_url": "https://github.com/eaquigley",
      "followers_url": "https://api.github.com/users/eaquigley/followers",
      "following_url": "https://api.github.com/users/eaquigley/following{/other_user}",
      "gists_url": "https://api.github.com/users/eaquigley/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/eaquigley/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/eaquigley/subscriptions",
      "organizations_url": "https://api.github.com/users/eaquigley/orgs",
      "repos_url": "https://api.github.com/users/eaquigley/repos",
      "events_url": "https://api.github.com/users/eaquigley/events{/privacy}",
      "received_events_url": "https://api.github.com/users/eaquigley/received_events",
      "type": "User",
      "site_admin": false
    },
    "open_issues": 0,
    "closed_issues": 412,
    "state": "closed",
    "created_at": "2014-07-09T15:34:37Z",
    "updated_at": "2014-08-15T18:18:04Z",
    "due_on": "2014-06-18T07:00:00Z"
  }''')