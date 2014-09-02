from django.db import models
from model_utils.models import TimeStampedModel

from apps.repositories.models import Repository
from apps.repositories.github_url_helper import get_github_view_url


GITHUB_TIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%SZ'

class Milestone(TimeStampedModel):
    """
    Information from API call: https://api.github.com/repos/iqss/dataverse/milestones
    """
    repository = models.ForeignKey(Repository)

    # START: correspond to github fields
    #
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    markdown_description = models.TextField(blank=True)

    # convert "state" attribute to this variable
    is_open = models.BooleanField(default=True)
    
    # github 'id' and 'number' fields
    github_id = models.IntegerField(db_index=True, unique=True)
    github_number = models.IntegerField()

    # issue counts
    open_issues = models.IntegerField()
    closed_issues = models.IntegerField()

    due_on = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    #
    # END: correspond to github fields
    
    last_retrieval_time = models.DateTimeField()

    def __unicode__(self):
        return '%s: %s' % (self.repository, self.title)
    
    def __str__(self):
        return self.__unicode__()
    
    def save(self, *args, **kwargs):
        # do something...
        super(Milestone, self).save(*args, **kwargs)

    def get_view_open_issues_url(self):
        return get_github_view_url(self)

    def get_view_closed_issues_url(self):
        #print 'get_github_view_url(self, is_closed=True)', get_github_view_url(self, is_closed=True)
        return get_github_view_url(self, is_closed=True)

    class Meta:
        ordering = ('repository', 'due_on', 'title')

    