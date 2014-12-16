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
    list_display = ('github_name', 'display_name', 'organization', 'display_order', 'is_visible', 'is_private','parent_repository', 'alt_title_display_name', 'last_retrieval_time', 'homepage')
    list_editable = ('display_order', 'is_visible', 'parent_repository')
    list_filter = ('is_visible', 'is_private', 'parent_repository',  'organization', )
    search_fields = ('github_name', 'organization__github_name')
    readonly_fields = ('modified', 'created')
    #filter_horizontal = ('sub_repos',)
admin.site.register(Repository, RepositoryAdmin)
