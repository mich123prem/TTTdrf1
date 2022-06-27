from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Zone, Activity, ActivityZone, Project, Counting, Observer
from guardian.admin import GuardedModelAdmin, UserObjectPermissionsForm
from guardian.shortcuts import get_objects_for_user
# Register your models here.
#admin.site.register(Permission)
@admin.register(Project)
class ProjectAdmin(GuardedModelAdmin): #UserObjectPermissionsForm):
    list_display = ('name',)

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        data=self.get_model_objects(request)
        return data

    def has_permission(self, request, obj, action):
        opts=self.opts
        # Which permission_model are we working on now?
        code_name = f'{action}_{opts.model_name}'
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return self.get_model_objects(request).exists()

    def get_model_objects(self, request, action=None, klass=None):
        opts=self.opts
        actions=[action] if action else ['view', 'change', 'add', 'delete'] #,'edit' ('change'?), 'delete'
        klass=klass if klass else opts.model
        model_name=klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

    def has_view_permissions(self, request, obj=None): #_change_ , _delete_
        return self.has_permission(request, obj, 'view')
    def has_change_permissions(self, request, obj=None): #_change_ , _delete_
        return self.has_permission(request, obj, 'change')
    def has_delete_permissions(self, request, obj=None): #_change_ , _delete_
        return self.has_permission(request, obj, 'delete')
    def has_add_permissions(self, request, obj=None): #_change_ , _delete_
        return self.has_permission(request, obj, 'add')


"""
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):

        qs = super().get_queryset(request)
        return qs.select_related('content_type')
"""
#admin.site.register(Project, ProjectAdmin)

admin.site.register(Zone)
admin.site.register(Activity)
admin.site.register(ActivityZone)
#admin.site.register(Project)
admin.site.register(Counting)
admin.site.register(Observer)