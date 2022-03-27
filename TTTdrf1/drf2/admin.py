from django.contrib import admin
from .models import Zone, Activity, ActivityZone, Project, Counting
# Register your models here.

admin.site.register(Zone)
admin.site.register(Activity)
admin.site.register(ActivityZone)
admin.site.register(Project)
admin.site.register(Counting)