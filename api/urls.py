__author__ = 'zhangzebo'
from django.conf.urls import patterns, url
from api.views import auth

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^user/$', user),
    url(r'^mantainUser/$', mantainUser),
    url(r'^SMScode/$', SMScode),
    url(r'^shop4S/',shop4S),
    url(r'^auth/',auth),
    url(r'^VIPCard/',VIPCard),
    url(r'^order',order),
    url(r'^taskOrder',taskOrder),
    url(r'^taskPre',taskPre),
    url(r'^taskNext',taskNext),
    url(r'^editorTask',editorTask),
    url(r'^taskPause',taskPause),
    url(r'^taskResume',taskResume),
    url(r'^ShopActivity',ShopActivity),
    url(r'^userCare',userCare),
    url(r'^component',component),
    url(r'^userMessage/',userMessage,name="userMessage"),

)