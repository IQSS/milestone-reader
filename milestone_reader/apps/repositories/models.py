from django.db import models
from django.db import models

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.conf import settings

from model_utils.models import TimeStampedModel
from apps.repositories.github_url_helper import get_github_api_milestones_url, get_github_view_url


class Organization(TimeStampedModel):
    """
    This is official information from GitHub
    e.g. https://api.github.com/orgs/iqss
    """
    github_login = models.CharField(max_length=255, help_text='"login" in the API call. Example: "IQSS"')
    github_name = models.CharField(max_length=255, help_text='Example: "Institute for Quantitative Social Science"')
    github_id = models.IntegerField()
    homepage = models.URLField(blank=True)

    def __unicode__(self):
        return self.github_login
        

class Repository(TimeStampedModel):
    """GeoConnect - For working with a Dataverse File for a given user
    These objects will persist for a limited time (days, weeks), depending on the system demand
    """
    github_name = models.CharField(max_length=255, help_text='dataverse')
    organization = models.ForeignKey(Organization)

    github_id = models.IntegerField()

    is_visible = models.BooleanField(default=True)

    display_order = models.IntegerField(default=10)

    description = models.TextField(blank=True, help_text='auto-filled')
    homepage = models.URLField(blank=True, help_text='auto-filled')
    
    last_retrieval_time = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.github_name
        
    class Meta:
        verbose_name_plural = 'Repositories'
        ordering = ('display_order', 'github_name' )
        
    def get_github_api_url(self):
        return get_github_api_milestones_url(self)
    
    