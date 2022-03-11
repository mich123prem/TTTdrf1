from django.contrib import admin
from .models import Zone, Activity, ActivityZone
# Register your models here.

admin.site.register(Zone)
admin.site.register(Activity)
admin.site.register(ActivityZone)