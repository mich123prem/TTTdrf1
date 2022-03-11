from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Zone, Activity, ActivityZone


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

#class ZoneSerializer(serializers.)
class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields=['lettername', 'sequencenumber', 'description', 'comment', 'activity']
        depth = 1

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['code', 'description' ]
        depth = 1

class ActivityZoneSerializer(serializers.ModelSerializer):

    fields = ActivitySerializer(source='activityzone_set', many=True)
    class Meta:
        model = ActivityZone
        fields = ['activity', 'zone', 'startTime', 'countingUser', 'numberOfVisitors']
        depth = 1

"""
activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    startTime = models.DateTimeField(auto_now=False) # App registers time
    countingUser = models.IntegerField() # **TODO: foreign key to a user
    numberOfVisitors = models.IntegerField() # THE COUNT ITSELF

"""