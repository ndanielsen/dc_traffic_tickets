from django.conf.urls import include, url

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'parkingviolations', views.ParkingViolationSet, 'parkingviolations')
router.register(r'status', views.ApiStatusViewSet, "status")

urlpatterns = [
    # Examples:
    # url(r'^$', 'dctraffic_project.views.home', name='home'),
    url(r'', include(router.urls)),
    url(r'', include('rest_framework.urls', namespace='rest_framework'))
    ]
