from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'team16project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', 'securecontactapp.views.home', name='home'),
    url(r'^reports/$', 'securecontactapp.views.reports', name='reports'),
    url(r'^reports/search/$', 'securecontactapp.views.search', name='search'),
    url(r'^reports/edit/([0-9]+)/$', 'securecontactapp.views.edit_report', name='edit_report'),
    url(r'^folder/$', 'securecontactapp.views.folder', name='folder'),
    url(r'^messages/$', 'securecontactapp.views.messages', name='messages'),
    url(r'^groups/$', 'securecontactapp.views.groups', name='groups'),
    url(r'^account/$', 'securecontactapp.views.account', name='account'),
    url(r'^register/$', 'securecontactapp.views.registration', name='register'),
    url(r'^check_login/$', 'securecontactapp.views.check_login', name='check_login'),
    url(r'^humans/$', 'securecontactapp.views.humans', name='humans'),
    url(r'^get_reports/$', 'securecontactapp.views.get_reports', name='get_reports'),
    url(r'^site_manager/$', 'securecontactapp.views.site_manager', name='site_manager'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
