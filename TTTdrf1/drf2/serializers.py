from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Zone, Activity, ActivityZone, Project, Counting
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

        fields=['lettername', 'observerName' ,'sequencenumber', 'description', 'comment', 'activity', 'project']

        depth = 1

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description' ]
        depth = 1

class CountingSerializer(serializers.ModelSerializer):
    #fields = ProjectSerializer( source='counting_set', many=True ) # TODO ** ?
    startTime=serializers.DateTimeField(format="iso-8601", required=True)
    class Meta:
        model=Counting
        fields=['project', 'startTime' , 'observerName']
