from django.contrib import admin

from apps.milestones.models import Milestone


class MilestoneAdmin(admin.ModelAdmin):    
    save_on_top = True
    list_display = ('title', 'repository', 'is_open', 'github_due_date', 'num_open_issues', 'github_updated_at', 'last_retrieval_time')
    list_filter = ( 'is_open', 'repository', )
    search_fields = ('title', 'description', 'repository__github_name')
    readonly_fields = ('modified', 'created')
admin.site.register(Milestone, MilestoneAdmin)
