from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from .models import Zone, Activity, ActivityZone, Project, Counting, Observer
# ** TODO: USE dataclass serializer ? https://github.com/oxan/djangorestframework-dataclasses

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ActivitySerializer(serializers.ModelSerializer):


    class Meta:
        model = Activity
        fields = ['code', 'description' ]
        depth = 1


class ActivityZoneSerializer(serializers.ModelSerializer):

    fields = ActivitySerializer(source='activityzone_set', many=True)
    #startTime=serializers.DateTimeField(format="iso-8601", required=False)
    class Meta:
        model = ActivityZone
        fields = ['activity', 'zone', 'countingUser', 'numberOfVisitors']
        depth = 1


class ZoneSerializer(serializers.ModelSerializer):
    #Zones will be copied (created) for each counting project
    class Meta:
        model = Zone
        # Zone will have a limited number of activities while activity can have "endless" zones
        fields=['id', 'lettername', 'observerName' ,'sequencenumber', 'description', 'comment', 'activities', 'project']
        depth = 1

class ObserverSerializer(serializers.ModelSerializer):
    # To be removed when users are properly in action
    class Meta:
        model = Observer
        #
        fields = ['observerName']
        depth = 1


class ProjectSerializer(serializers.ModelSerializer, ):
    activities=ActivitySerializer(many=True)
    zones=ZoneSerializer(many=True)
    observers = ObserverSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'activities', 'zones', 'observers', ]
        depth = 1

    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        readers = Group.objects.get(name='readers')
        supervisors = Group.objects.get(name='supervisors')

        return {
            'view_post': [current_user, readers],
            'change_post': [current_user],
            'delete_post': [current_user, supervisors]
        }


class CountingSerializer(serializers.ModelSerializer):
    #fields = ProjectSerializer( source='counting_set', many=True ) # TODO ** ?
    startTime=serializers.DateTimeField(format="iso-8601", required=True)
    class Meta:
        model=Counting
        fields=['project', 'startTime' , 'observerName']
