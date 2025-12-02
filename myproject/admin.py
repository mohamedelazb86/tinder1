from django.contrib import admin


from .models import Project,ProjectAction,ProjectItem
admin.site.register(Project)
admin.site.register(ProjectAction)
admin.site.register(ProjectItem)
