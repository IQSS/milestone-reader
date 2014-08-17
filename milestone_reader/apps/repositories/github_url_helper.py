
GITHUB_VIEW_URL_BASE = 'https://github.com'
GITHUB_API_URL_BASE = 'https://api.github.com'
def urljoin(*parts):
    return "/".join(map(lambda x: str(x).rstrip('/'), parts))
    
def get_github_view_url(github_obj):
    if github_obj is None:
        return None
    
    class_name = github_obj.__class__.__name__
    if class_name == 'Milestone':
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , github_obj.repository.organization.github_name\
                    , github_obj.repository.github_name\
                    , github_obj.github_name)
    elif class_name == 'Repository':
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , github_obj.organization.github_name\
                    , github_obj.github_name)
    elif class_name == 'Organization':
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , github_obj.github_name)
    return None
    
def get_github_api_milestones_url(repository):
    print 'repository', repository
    """
    Given a repository project, return a url with this structure:
    
        https://api.github.com/repos/{{ organization }}/{{ repository }}/milestones?state=all
        https://api.github.com/repos/iqss/dataverse/milestones?state=all

    :param repository: repositories.models.repository
    :returns: str representing github api url
    """
    if not repository.__class__.__name__ == 'Repository':
        return None
        
    return urljoin(GITHUB_API_URL_BASE\
                    , 'repos'
                    , repository.organization.github_login\
                    , repository.github_name
                    , 'milestones?state=all')
                    