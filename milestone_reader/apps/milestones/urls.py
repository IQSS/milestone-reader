from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.milestones.views',

    url(r'^by-due-date/(?P<repo_name>(\-|_|\w){1,120})/$', 'view_by_due_date', name="view_repo_by_due_date"),
    
    url(r'^by-due-date/$', 'view_by_due_date', name="view_by_due_date"),

    url(r'^milestone-roadmap/$', 'view_by_columns', name="view_by_columns"),

    url(r'^milestone-roadmap/(?P<repo_name>(\-|_|\w){1,120})/$', 'view_single_repo_column', name="view_single_repo_column"),
)

urlpatterns += patterns('apps.milestones.views_history',

    url(r'^milestone-history/$', 'view_milestone_history', name="view_milestone_history"),

    url(r'^milestone-history/(?P<chosen_year>(\d){4})/$', 'view_milestone_history', name="view_milestone_history_by_year"),

    #url(r'^milestone-roadmap/(?P<repo_name>(\-|_|\w){1,120})/$', 'view_single_repo_column', name="view_single_repo_column"),

)
