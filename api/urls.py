from django.conf.urls import include, url

from rest_framework import routers

from api import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'parkingviolations', views.ParkingViolationSet, 'parkingviolations')
router.register(r'status', views.ApiStatusViewSet, "status")

snippet_list = views.ParkingViolationsNearProximity.as_view({
    'get': 'post',
    # 'post': 'create'
})


urlpatterns = [
    # Examples:
    # url(r'^$', 'dctraffic_project.views.home', name='home'),
    url(r'', include(router.urls)),
    url(r'nearest', snippet_list, name='nearest'),
    url(r'', include('rest_framework.urls', namespace='rest_framework'))
    ]
