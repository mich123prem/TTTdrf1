from django.contrib import admin
from .models import Zone, Activity, ActivityZone, Project, Counting, Observer
from guardian.admin import GuardedModelAdmin
# Register your models here.

class ProjectAdmin(GuardedModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

admin.site.register(Zone)
admin.site.register(Activity)
admin.site.register(ActivityZone)
#admin.site.register(Prcdoject)
admin.site.register(Counting)
admin.site.register(Observer)