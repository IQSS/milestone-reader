from __future__ import print_function

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

from milestone_reader.utils.msg_util import *

from apps.repositories.models import Repository
from apps.milestones.models import Milestone

from apps.milestones.view_helper import MilestoneMonthOrganizer, RepoMilestoneMonthsOrganizer

def get_basic_milestone_params():
    return dict(is_open=True\
                , repository__is_visible=True)

def view_by_columns(request):
    """
    http://127.0.0.1:8000/milestones/by-columns/
    :param request:
    :return:
    """
    filter_params = get_basic_milestone_params()

    milestones = Milestone.objects.select_related('repository', 'repository__organization', 'parent_repository'\
                                ).filter(**filter_params\
                                ).order_by('due_on')

    mmo = MilestoneMonthOrganizer(milestones)
    #mmo.show()
    #return HttpResponse('ok')
    d = {}

    d['page_title'] = 'IQSS Data Science Projects: Milestones'
    d['sorted_repos'] = mmo.get_sorted_repos()
    d['organized_months'] = mmo.get_organized_months()
    d['NO_DUE_DATE'] = RepoMilestoneMonthsOrganizer.NO_DUE_DATE
    d['milestone_count'] = milestones.count()
    print(d)
    return render_to_response('milestones/view_by_column.html'\
                              , d\
                              , context_instance=RequestContext(request))


def view_by_due_date(request, repo_name=None):
    """Sample view/template
    http://127.0.0.1:8000/milestones/by-due-date/
    """
    filter_params = get_basic_milestone_params()

    if repo_name:
        filter_params['repository__github_name'] = repo_name
    else:
        repo_name = None
        
    milestones = Milestone.objects.select_related('repository', 'repository__organization'\
                                ).filter(**filter_params\
                                ).order_by('due_on')
                                
    d = {}
    d['page_title'] = 'IQSS Data Science Projects: Milestones'
    d['repos'] = Repository.objects.select_related('organization').filter(is_visible=True)
    d['milestones'] = milestones
    d['milestone_count'] = milestones.count()
    d['chosen_repository'] = repo_name
    if repo_name is None:
       d['ALL_REPOS'] = True
        
    return render_to_response('milestones/view_by_due_date.html'\
                              , d\
                              , context_instance=RequestContext(request))

    