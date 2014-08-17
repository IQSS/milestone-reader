from django.contrib import admin
from apps.repositories.models import Organization, Repository

class OrganizationAdmin(admin.ModelAdmin):    
    save_on_top = True
    list_display = ('github_login', 'github_name', 'github_id', 'homepage', 'modified')
    search_fields = ('github_login', 'github_name',)
    readonly_fields = ('modified', 'created')
admin.site.register(Organization, OrganizationAdmin)


class RepositoryAdmin(admin.ModelAdmin):    
    save_on_top = True
    list_display = ('github_name', 'organization', 'display_order', 'is_visible', 'last_retrieval_time', 'homepage')
    list_editable = ('display_order',)
    list_filter = ('is_visible', 'organization', )
    search_fields = ('github_name', 'organization__github_name')
    readonly_fields = ('modified', 'created')
admin.site.register(Repository, RepositoryAdmin)

