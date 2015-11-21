from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'team16project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', 'securecontactapp.views.home', name='home'),
    url(r'^reports/$', 'securecontactapp.views.reports', name='reports'),
    url(r'^messages/$', 'securecontactapp.views.messages', name='messages'),
    url(r'^groups/$', 'securecontactapp.views.groups', name='groups'),
    url(r'^account/$', 'securecontactapp.views.account', name='account'),
    url(r'^register/$', 'securecontactapp.views.registration', name='register'),
    url(r'^check_login/$', 'securecontactapp.views.check_login', name='check_login'),
    url(r'^humans/$', 'securecontactapp.views.humans', name='humans'),
)
