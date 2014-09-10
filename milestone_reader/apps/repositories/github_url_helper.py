import urllib

GITHUB_VIEW_URL_BASE = 'https://github.com'
GITHUB_API_URL_BASE = 'https://api.github.com'

def urljoin(*parts):
    return "/".join(map(lambda x: str(x).rstrip('/'), parts))


def get_view_repository_milestones_url(repo):
    if not repo.__class__.__name__=='Repository':
        return None

    return urljoin(get_github_view_url(repo), 'milestones')

def get_github_view_url(github_obj, is_closed=False):
    if github_obj is None:
        return None
    
    class_name = github_obj.__class__.__name__
    if class_name == 'Milestone':

        if is_closed:
            # https://github.com/IQSS/geoconnect/issues?q=is:closed+milestone:"{ milestone title }"+
            return urljoin(GITHUB_VIEW_URL_BASE\
                        , github_obj.repository.organization.github_login\
                        , github_obj.repository.github_name\
                        , 'issues?q=is:closed+milestone:"%s"' %  urllib.quote((github_obj.title))\
                    )
            
            
        # https://github.com/IQSS/geoconnect/milestones/{ milestone name }
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , github_obj.repository.organization.github_login\
                    , github_obj.repository.github_name\
                    , 'milestones'\
                    , urllib.quote(github_obj.title))
        
                    
    elif class_name == 'Repository':
        # https://api.github.com/repos/IQSS/dataverse
        return urljoin(GITHUB_VIEW_URL_BASE\
                    #, 'repos'\
                    , github_obj.organization.github_login\
                    , github_obj.github_name)
                    
    elif class_name == 'Organization':
        # https://api.github.com/orgs/IQSS
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , 'orgs'\
                    , github_obj.github_name)
    return None


def get_github_api_repository_url(repository, milestones=True):
    #print 'repository', repository
    """
    Given a repository project, return a url with this structure:
    
        https://api.github.com/repos/{{ organization }}/{{ repository }}/milestones?state=all
        https://api.github.com/repos/iqss/dataverse/milestones?state=all

    :param repository: repositories.models.repository
    :returns: str representing github api url
    """
    if not repository.__class__.__name__ == 'Repository':
        return None
    
    api_url = urljoin(GITHUB_API_URL_BASE\
                    , 'repos'
                    , repository.organization.github_login\
                    , repository.github_name)
                    
    if milestones is True:
        api_url = urljoin(api_url
                    , 'milestones?state=all')
    
    return api_url
                    