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

from apps.milestones.views import get_issue_counts_query_base

    
    
def get_basic_milestone_history_query(chosen_year=None):
    """
    Show all tickets from current month onwards: open and closed tickets

    Default to the current year
    """
    current_date = datetime.today()

    if chosen_year is None or not type(chosen_year) is int:
        chosen_year = current_date.year
        
    filter_params = { #'due_on__gte' : datetime(year=chosen_year, month=1, day=1)\
            #,
             'repository__is_visible' : True\
            }
            
    if chosen_year == current_date.year:   # For the current year, show months previous to the current month
        filter_params.update({ 'due_on__lt': datetime(year=chosen_year, month=current_date.month, day=1) })
    else:
        filter_params.update({ 'due_on__year': chosen_year })
        # For previous years, show full year
        #filter_params.update({ 'due_on__lte': datetime(year=year, month=12, day=31) })
                
        
    
    return (chosen_year, \
                Milestone.objects.select_related('repository', 'repository__organization', 'repository__parent_repository'\
                                ).filter(**filter_params)\
            )                
    

def view_milestone_history(request, chosen_year=None):
    """
    http://127.0.0.1:8000/milestones/by-columns/
    :param request:
    :return:
    """    
    (chosen_year, basic_query) = get_basic_milestone_history_query(chosen_year)
    
    milestones = basic_query.order_by('due_on')

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

    d['page_title'] = 'Milestone History for %s' % chosen_year
    d['chosen_year'] = chosen_year
    d['last_retrieval_time'] = last_retrieval_time
    d['sorted_repos'] = sorted_repos
    d['organized_months'] = mmo.get_organized_months(descending_order=True)
    d['NO_DUE_DATE'] = RepoMilestoneMonthsOrganizer.NO_DUE_DATE
    d['milestone_count'] = milestones.count()
    d['num_open_issues'] = num_open_issues
    d['num_closed_issues'] = num_closed_issues

    d['hide_description'] = True
    print(d)
    return render_to_response('milestones/view_history_multi_column.html'\
                              , d\
                              , context_instance=RequestContext(request))

