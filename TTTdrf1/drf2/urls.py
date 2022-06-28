from django.urls import path, re_path, include
#from django.conf.urls import pattern,
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ActivityViewSet, ZoneViewSet, ProjectViewSet, \
    ActivityList, CountingViewSet, ProjectByName, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router=DefaultRouter()
router.register("zone", ZoneViewSet, basename="zone")
router.register("activity", ActivityViewSet, basename="activity")
router.register("project", ProjectViewSet, basename="project")
router.register("counting", CountingViewSet, basename="counting")
urlpatterns = [
   re_path('projectByName/(?P<name>[a-zA-Z0-9]+)',ProjectViewSet.as_view({'get':'retrieve'})),
   path('project/<int:pk>', ProjectViewSet.as_view({'get':'get'})),
   path('activities/', ActivityList.as_view()),
   path('users/', UserViewSet.as_view({'get': 'list'})),
#    path('drf2/<int:pk>/', views.SnippetDetail.as_view()),
    path('', include(router.urls)),

    # to be able to fetch token with user/pass
    path('api-token-auth/', views.ObtainAuthToken.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)