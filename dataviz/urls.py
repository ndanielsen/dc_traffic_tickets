from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'dctraffic_project.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name="empty.html"), name='home'),
    url(r'^sandbox1/', TemplateView.as_view(template_name="sandbox1.html"), name='sandbox1'),
    url(r'^sandbox2/', TemplateView.as_view(template_name="sandbox2.html"), name='sandbox2'),
    url(r'^sandbox3/', TemplateView.as_view(template_name="sandbox3.html"), name='sandbox3'),
    url(r'^sandbox4/', TemplateView.as_view(template_name="sandbox4.html"), name='sandbox4'),
    ]
