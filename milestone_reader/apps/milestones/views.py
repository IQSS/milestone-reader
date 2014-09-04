from __future__ import print_function

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from django.db.models import Q

from milestone_reader.utils.msg_util import *
from datetime import datetime
from apps.repositories.models import Repository
from apps.milestones.models import Milestone

from apps.milestones.view_helper import MilestoneMonthOrganizer, RepoMilestoneMonthsOrganizer


def get_issue_counts_query_base(chosen_repo=None):

    # These counts are irrespective of date    
    if chosen_repo is not None:
        return Milestone.objects.select_related('repository').filter(repository__is_visible=True).filter(Q(repository=chosen_repo)|Q(repository__parent_repository=chosen_repo))
    else:
        return Milestone.objects.select_related('repository').filter(repository__is_visible=True)
    
    
def get_basic_milestone_query():
    """
    Show all tickets from current month onwards: open and closed tickets
    """
    
    current_time = datetime.today()
    current_month = datetime(current_time.year, current_time.month, 1)

    
    return Milestone.objects.select_related('repository', 'repository__organization', 'repository__parent_repository'\
                                ).filter(due_on__gte=current_month\
                                       , repository__is_visible=True\
                                )
    
    # original query of only open milestones
    #return Milestone.objects.select_related('repository', 'repository__organization', 'repository__parent_repository'\
    #                            ).filter(is_open=True\
    #                                   , repository__is_visible=True\
    #                            )


def get_basic_milestone_params():
    return dict(is_open=True\
                , repository__is_visible=True)

def view_by_columns(request):
    """
    http://127.0.0.1:8000/milestones/by-columns/
    :param request:
    :return:
    """
    milestones = get_basic_milestone_query().order_by('due_on')

    open_closed_cnts = get_issue_counts_query_base().values('open_issues', 'closed_issues')
    num_open_issues = sum(x['open_issues'] for x in open_closed_cnts)
    num_closed_issues = sum( x['closed_issues'] for x in open_closed_cnts)

    mmo = MilestoneMonthOrganizer(milestones)
    #mmo.show()
    #return HttpResponse('ok')
    sorted_repos = mmo.get_sorted_repos()
    if sorted_repos and len(sorted_repos) > 0:
        last_retrieval_time = sorted_repos[0].last_retrieval_time
    else:
        last_retrieval_time = None

    d = {}

    d['page_title'] = 'Current Project Milestones'
    d['last_retrieval_time'] = last_retrieval_time
    d['sorted_repos'] = sorted_repos
    d['organized_months'] = mmo.get_organized_months()
    d['NO_DUE_DATE'] = RepoMilestoneMonthsOrganizer.NO_DUE_DATE
    d['milestone_count'] = milestones.count()
    d['num_open_issues'] = num_open_issues
    d['num_closed_issues'] = num_closed_issues

    d['hide_description'] = True
    print(d)
    return render_to_response('milestones/view_multi_column.html'\
                              , d\
                              , context_instance=RequestContext(request))


def view_single_repo_column(request, repo_name):
    """
    Show milestones from this repository and any child repositories (direct children, e.g. 1-level)
    :param request:
    :param repo_name:
    :return:
    """
    milestones = get_basic_milestone_query()#.order_by('due_on')

    try:
        chosen_repo = Repository.objects.select_related('organization', 'parent_repository').get(is_visible=True, github_name=repo_name)
    except Repository.DoesNotExist:
        raise Http404("Repository not found: %s" % repo_name)

    # Repository has no parent -- so it is a parent
    # Pull milestones:
    #   - from this repository  (e.g. dataverse)
    #   - any repositories that have this repo as a parent  (e.g. geoconnect)
    #
    if not chosen_repo.parent_repository:
        milestones = milestones.filter(Q(repository=chosen_repo)|Q(repository__parent_repository=chosen_repo))
    else:
        # This is a child repository, only show its milestones
        milestones = milestones.filter(repository=chosen_repo)

    milestones_list = list(milestones.order_by('due_on'))

    current_date = datetime.now()
    for ms in milestones_list:
        if ms.due_on:
            ms.days_remaining = ms.due_on.replace(tzinfo=None) - current_date#.date()


    #open_closed_cnts = milestones.values('open_issues', 'closed_issues')
    open_closed_cnts = get_issue_counts_query_base(chosen_repo).values('open_issues', 'closed_issues')
    num_open_issues = sum(x['open_issues'] for x in open_closed_cnts)
    num_closed_issues = sum( x['closed_issues'] for x in open_closed_cnts)

    d = {}

    d['repos'] = Repository.objects.select_related('organization', 'parent_repository').filter(parent_repository__isnull=True).filter(is_visible=True)

    d['page_title'] = 'Current Milestones: %s' % chosen_repo
    d['page_title_link'] = chosen_repo.get_github_view_url()
    #d['page_title_link'] = chosen_repo.get_github_view_milestones_url()

    d['chosen_repository'] = chosen_repo
    d['milestone_count'] = len(milestones_list)#.count()
    d['milestones'] = milestones_list

    d['num_open_issues'] = num_open_issues
    d['num_closed_issues'] = num_closed_issues

    d['SINGLE_COLUMN'] = True
    #print(d)
    return render_to_response('milestones/view_single_repo_column.html'\
                              , d\
                              , context_instance=RequestContext(request))




def view_by_due_date(request, repo_name=None):
    """Sample view/template
    http://127.0.0.1:8000/milestones/by-due-date/
    """
    milestones = get_basic_milestone_query()

    if repo_name:
        milestones = milestones.filter(repository__github_name=repo_name)
    else:
        repo_name = None
        
    milestones = milestones.order_by('due_on')
                                
    d = {}
    d['page_title'] = 'IQSS Data Science Projects: Milestones'
    d['page_title_link'] = 'http://datascience.iq.harvard.edu'

    d['repos'] = Repository.objects.select_related('organization').filter(is_visible=True)
    d['milestones'] = milestones
    d['milestone_count'] = milestones.count()
    d['chosen_repository'] = repo_name
    if repo_name is None:
       d['ALL_REPOS'] = True
        
    return render_to_response('milestones/view_by_due_date.html'\
                              , d\
                              , context_instance=RequestContext(request))

    