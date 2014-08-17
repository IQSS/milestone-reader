from django.db import models
from model_utils.models import TimeStampedModel

from apps.repositories.models import Repository
from apps.repositories.github_url_helper import get_github_api_milestones_url, get_github_view_url


    
class Milestone(TimeStampedModel):
    """
    Information from API call: https://api.github.com/repos/iqss/dataverse/milestones
    """
    repository = models.ForeignKey(Repository)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    is_open = models.BooleanField(default=True)
    
    github_id = models.IntegerField(db_index=True)
    github_number = models.IntegerField()

    num_open_issues = models.IntegerField()
    num_closed_issues = models.IntegerField()

    github_due_date = models.DateTimeField(blank=True, null=True)
    github_updated_at = models.DateTimeField()
    
    last_retrieval_time = models.DateTimeField()

    def __unicode__(self):
        return '%s: %s' % (self.repository, self.title)
    
    def __str__(self):
        return self.__unicode__
    
    def save(self, *args, **kwargs):
        # do something...
        super(Milestone, self).save(*args, **kwargs)
        
    def get_view_milestone_url(self):
        return get_github_view_url(self)

    def get_github_api_url(self):
        return get_github_api_milestones_url(self)
        
    class Meta:
        ordering = ('repository', 'github_due_date', 'title')

    