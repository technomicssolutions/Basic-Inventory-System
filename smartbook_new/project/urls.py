from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings


from project.views import *

urlpatterns = patterns('',
	url(r'create_project/$', CreateProject.as_view(), name='create_project'),
	url(r'projects/$', Projects.as_view(), name='projects'),
	url(r'add_item/$', AddItem.as_view(), name='add_item'),
	url(r'project_items/$', ProjectItemList.as_view(), name='project_items'),
	url(r'items/$', ItemList.as_view(), name='items'),
	url(r'service_charges/$', ServiceChargeList.as_view(), name='service_charges'),
)