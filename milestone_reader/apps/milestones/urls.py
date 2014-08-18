from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.milestones.views',

    url(r'^by-due-date/(?P<repo_name>(\-|_|\w){1,120})/$', 'view_by_due_date', name="view_repo_by_due_date"),
    
    url(r'^by-due-date/$', 'view_by_due_date', name="view_by_due_date"),

)
