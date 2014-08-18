from __future__ import print_function

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from apps.repositories.models import Repository
from apps.milestones.models import Milestone

def view_by_due_date(request, repo_name=None):
    
    filter_params = dict(is_open=True\
                        , repository__is_visible=True)
    if repo_name:
        filter_params['repository__github_name'] = repo_name

    milestones = Milestone.objects.select_related('repository', 'repository__organization'\
                                ).filter(**filter_params\
                                ).order_by('due_on')
                                
    d = {}
    d['repos'] = Repository.objects.select_related('organization').filter(is_visible=True)
    d['page_title'] = 'Open Milestones'
    d['milestones'] = milestones
    d['milestone_count'] = milestones.count()
    d['chosen_repository'] = repo_name
    
    return render_to_response('milestones/view_by_due_date.html'\
                              , d\
                              , context_instance=RequestContext(request))

    