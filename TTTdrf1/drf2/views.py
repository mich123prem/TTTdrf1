from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from TTTdrf1.drf2.serializers import UserSerializer, GroupSerializer, ActivitySerializer, ZoneSerializer, \
    ProjectSerializer
from .models import Activity, Zone, ActivityZone, Project
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# **TODO: Check references to drf1. maybe rename it to avoid confusion?

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def createActivityZone(activity_item, zone_obj, activity_obj):
        # ** TODO: Check if a registration is actually new, or a close enough in time registration already exists

        # ** TODO: Shall we split date and time?
        try:
            activity_zone_obj=ActivityZone.objects.get(activity=activity_obj, zone=zone_obj)
        except:
            activity_zone_obj=ActivityZone.objects.create(activity=activity_obj,
                                                zone=zone_obj, startTime=activity_item["startTime"])
        activity_zone_obj.numberOfVisitors=activity_item["numberOfVisitors"]
        #activity_zone_obj.startTime=activity_item["startTime"]
        return activity_zone_obj

class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    serializer_class = ActivitySerializer

    def get_queryset(self):
        activity = Activity.objects.all()  # can also use other methods, like get() or complexFilter
        return activity

    # ** DO WE ACTUALLY NEED THIS? Both activities and zones will be created from the admin.
    def create(self, request, *args, **kwargs):
        data = request.data
        new_activity = Activity.objects.create(
            code=data["code"],
            description=data['description'],
            comment=data['comment'])
        new_activity.save()
        serializer = ActivitySerializer(new_activity)
        return Response(serializer.data)


class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    serializer_class = ZoneSerializer

    def get_queryset(self):
        zone = Zone.objects.all()  # can also use other methods, like get() or complexFilter
        return zone
    # TODO: **Trenger vi egentlig denne? activityZones bare brukes i prosjekter
    def createActivityZone(self, activity_item, zone_obj, activity_obj):
        # ** TODO: Check if a registration is actually new, or a close enough in time registration already exists

        # ** TODO: Shall we split date and time?
        try:
            activity_zone_obj=ActivityZone.objects.get(activity=activity_obj, zone=zone_obj)
        except:
            activity_zone_obj=ActivityZone.objects.create(activity=activity_obj,
                                                zone=zone_obj)
        activity_zone_obj.numberOfVisitors=activity_item["numberOfVisitors"]
        activity_zone_obj.startTime=activity_item["startTime"]
        return activity_zone_obj
        """
        return activity_zone_obj.
            (activity=activity_obj,
                                           zone=zone_obj,  # .pk,
                                           startTime=activity_item["startTime"],
                                           numberOfVisitors=activity_item["numberOfVisitors"],
                                           countingUser=activity_item["countingUser"])
        """
    def create(self, request, *args, **kwargs):
        data = request.data
        # check if zone does not exist yet?
        try:
            zone_obj = Zone.objects.get(lettername=data["lettername"], sequencenumber=data['sequencenumber'],
                                        description=data['description'], comment=data['comment'])
        except:
            new_zone_obj = Zone.objects.create(lettername=data["lettername"], sequencenumber=data['sequencenumber'],
                                               description=data['description'], comment=data['comment'])
            new_zone_obj.save()
            zone_obj = new_zone_obj

        for activity_item in data["activity"]:
            activity_obj = Activity.objects.get(code=activity_item["code"])
            # print("activity_obj:", activity_obj)
            activityZone_obj = zone_obj.activityzone_set.get_or_create(activity_obj, zone_obj)#self.createActivityZone(activity_item, zone_obj, activity_obj)

            zone_obj.activity.add(activity_obj)

        serializer = ZoneSerializer(new_zone_obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pass

"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    startTime = models.DateTimeField(auto_now=False) # App registers time
    countingUser = models.IntegerField() # **TODO: foreign key to a user
    numberOfVisitors = models.IntegerField() # THE COUNT ITSELF

"""


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        projects = Project.objects.all()  # can also use other methods, like get() or complexFilter
        return projects

        # ** DO WE ACTUALLY NEED THIS? Both activities, zones and projects will be created from the admin GUI.

    def create(self, request, *args, **kwargs):
        data = request.data
        project_item=data["project"]
            # check if project does not exist yet?
        try:
            project_obj = Project.objects.get(name=project_item["name"])
        except:
            new_project_obj = Project.objects.create(name=project_item["name"])
            new_project_obj.save()
            project_obj = new_project_obj

        for zone_item in project_item["zone"]:
            zone_obj = Zone.objects.get(lettername=zone_item["lettername"],project=project_obj)
            print("zi=",zone_item)
            zone_obj.observerName=zone_item["observerName"]
            zone_obj.save()
            for activity_item in zone_item["activity"]:
                # WE ASSUME ACTIVITY EXISTS!!!
                #activityZone_obj=ActivityZone.objects.get_or_create(zone=zone_obj,)
                activity_obj=Activity.objects.get(code=activity_item["code"])
                activity_zone_obj = createActivityZone(activity_item, zone_obj, activity_obj) #zone_obj.activityzone_set.get_or_create(zone=zone_obj, activity=activity_obj)

                activity_zone_obj.numberOfVisitors = activity_item["numberOfVisitors"]
                activity_zone_obj.startTime = activity_item["startTime"]
                activity_zone_obj.save()
                #zone_obj.add(activity_zone_obj)
            #print("activity_obj:", activity_obj)

            #project_obj.add(zone_obj)





        serializer = ProjectSerializer(project_obj)
        return Response(serializer.data)


#########################################################################################
class ActivityList(APIView):
    """
    List all Activities, or create a new activity.
    """

    def get(self, request, format=None):
        activities = Activity.objects.all()  # Here we could use get, for getting only activities for a certain library?
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    # **TODO - do we need it?
    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetail(APIView):
    """
    Retrieve, update or delete a activity instance.
    """

    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActivityList(APIView):
    """
    List all Activities, or create a new activity.
    """

    def get(self, request, format=None):
        activities = Activity.objects.all()  # Here we could use get, for getting only activities for a certain library?
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    # **TODO - do we need it?
    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ZoneList(APIView):
#class FullProjectList(APIView):
