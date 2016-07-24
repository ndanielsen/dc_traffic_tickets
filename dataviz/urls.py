from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'dctraffic_project.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name="heatmap.html"), name='home'),
    ]
