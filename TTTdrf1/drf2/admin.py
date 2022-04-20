from django.contrib import admin
from .models import Zone, Activity, ActivityZone, Project, Counting
from guardian.admin import GuardedModelAdmin
# Register your models here.

class ProjectAdmin(GuardedModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

admin.site.register(Zone)
admin.site.register(Activity)
admin.site.register(ActivityZone)
#admin.site.register(Project)
admin.site.register(Counting)