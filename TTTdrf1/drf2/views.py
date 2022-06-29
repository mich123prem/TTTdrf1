from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_guardian import filters
from TTTdrf1.drf2.serializers import UserSerializer, GroupSerializer, ActivitySerializer, ZoneSerializer, \
    ProjectSerializer, CountingSerializer, ObserverSerializer
from TTTdrf1.drf2.models import Activity, Zone, ActivityZone, Project, Counting, Observer
from TTTdrf1.drf2.permissions import CustomObjectPermissions, ObjectOnlyPermissions

from pprint import pprint
from pprint import pprint

from django.contrib.auth.models import User, Group
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from TTTdrf1.drf2.models import Activity, Zone, ActivityZone, Project, Counting, Observer
from TTTdrf1.drf2.permissions import CustomObjectPermissions
from TTTdrf1.drf2.serializers import UserSerializer, GroupSerializer, ActivitySerializer, ZoneSerializer, \
    ProjectSerializer, CountingSerializer, ObserverSerializer

import inspect
import logging
logging.debug('Watch out!')
logger = logging.getLogger("oauth2")
# **TODO: Check references to drf1. maybe rename it to avoid confusion?

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CustomObjectPermissions]

    def retrieve(self, request, name=None, password=None ):
        logger.debug( "in retrieve:" )
        queryset= User.objects.all()
        user=get_object_or_404(queryset, name=name, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def createActivityZone(activity_item, zone_obj, activity_obj, counting_obj):
        # ** TODO: Check if a registration is actually new, or a close enough in time registration already exists

        # ** TODO: Shall we split date and time?

        activity_zone_obj=ActivityZone.objects.create(activity=activity_obj,
                                                zone=zone_obj, counting=counting_obj)
        activity_zone_obj.numberOfVisitors=activity_item["count"]

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
        #activity_zone_obj.startTime=activity_item["startTime"]
        return activity_zone_obj

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


class CountingViewSet(viewsets.ModelViewSet):
    #
    # A counting objects represents a single "trip" through all the
    # zones of the library, at a common timestamp (startTime).
    # Represents a particular registration sheet of the traditional excel-file
    #
    serializer_class = CountingSerializer

    def get_queryset(self):
        countings = Counting.objects.all()
        return countings

    def create(self, request, *args, **kwargs):
        data = request.data
        counting_item=data # **TODO: ["counting"] ?
        # check if project does not exist yet?
        #try: A COUNTING OBJECT IS ALWAYS NEW
            #counting_obj = Project.objects.get(name=project_item["name"])
        #except:
        project = Project.objects.get( pk=counting_item["project_id"] )  # counting_item["project_id"]),
        startTime=counting_item["timestamp"]
        counting_obj = Counting.objects.create(
            project=project,

            startTime=startTime,

            observerName = counting_item["observer_name"]
                                               )

        project.modified_at = startTime
        project.save()
        counting_obj.save()
        for zone_item in counting_item["ActivityZones"]:
            zone_obj = Zone.objects.get(pk=zone_item["zone_ID"]) # Or use zone name
            for activity_item in zone_item["Activities"]:
                # WE ASSUME ACTIVITY EXISTS!!!
                activity_obj=Activity.objects.get(code=activity_item["code"])
                activity_zone_obj = createActivityZone(activity_item, zone_obj, activity_obj, counting_obj) #zone_obj.activityzone_set.get_or_create(zone=zone_obj, activity=activity_obj)

                activity_zone_obj.numberOfVisitors = activity_item["count"]
                #activity_zone_obj.startTime = activity_item["startTime"]
                activity_zone_obj.save()
                #zone_obj.add(activity_zone_obj)

        serializer = CountingSerializer(counting_obj)
        return Response(serializer.data)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    serializer_class = ProjectSerializer
    permission_classes = [ObjectOnlyPermissions]
    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self, pk):
        try:
            obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
            self.check_object_permissions( self.request, obj )
            return obj
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def get_queryset(self):
        projects = Project.objects.all()  # can also use other methods, like get() or complexFilter
        return projects

        # ** DO WE ACTUALLY NEED THIS? Both activities, zones and projects will be created from the admin GUI.

    def create(self, request, *args, **kwargs):
        data = request.data
        project_id=data["project_id"]
            # check if project does not exist yet?
        try:
            project_obj = Project.objects.get(name="tonsberg22")#({"pk": project_id})#(name=project_item["name"])
        except:
            new_project_obj = Project.objects.create(name="tonsberg22")
            new_project_obj.save()
            project_obj = new_project_obj

        serializer = ProjectSerializer(project_obj)
        return Response(serializer.data)

    def perform_create(self):
        # ** TODO: IMPLEMENT THIS for restricted creation of objects
        return super().perform_create()

    def retrieve(self, request, name=None):
        logger.debug( "in retrieve:" )
        queryset= Project.objects.all()
        project=get_object_or_404(queryset, name=name)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)



class ObserverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    serializer_class = ObserverSerializer

    def get_queryset(self):
        observer = Observer.objects.all()  # can also use other methods, like get() or complexFilter
        return observer
    # TODO: **Trenger vi egentlig denne? activityZones bare brukes i prosjekter



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

# class ZoneList(APIView):
#class FullProjectList(APIView):
class ProjectDetail(APIView):
    """
    Retrieve, update or delete an activity-instance.
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class ProjectByName(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk=0, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class ProjectByUser(APIView):

    # How to chose default project to return to a user?
    #   - The last ('-modified_at') project the user has engaged with ?
    #   - The last ('-modified_at') project the user has permission to ?
    NotYetImplemented=True
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request):
        #GET THE LATEST PROJECT ASSOCIATED WITH CURRENT USER
        project=None
        queryset_list = list(Project.objects.all().order_by( '-modified_at' ))
        logger.warning("after queryset")
        if self.NotYetImplemented:
            project=self.get_object( 5 )
            serializer = ProjectSerializer( project )
            return Response( serializer.data )

        for po in queryset_list:
            # User has permissions?
            logger.warning("before if")
            if self.check_object_permissions(self.request, po):
                project=self.get_object(po.pk)
                logger.warning("Name="+project.name)


        serializer=ProjectSerializer(project)
        return Response(serializer.data)

