from django.urls import path, re_path, include
#from django.conf.urls import pattern,
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ActivityViewSet, ZoneViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("zone", ZoneViewSet, basename="zone")
router.register("activity", ActivityViewSet, basename="activity")
urlpatterns = [
#   path('drf1/', views.SnippetList.as_view()),
#    path('drf1/<int:pk>/', views.SnippetDetail.as_view()),
    path('', include(router.urls)),

]

#urlpatterns = format_suffix_patterns(urlpatterns)