from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User, Group, Permission

from securecontactapp.models import Reporter

from Crypto import Random
from Crypto.PublicKey import RSA


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

if not User.objects.filter(username='admin').exists():
    usr = User(username='admin', password='pbkdf2_sha256$20000$F0pHmzPSjX85$zAjUBXWVnbCdqoI8HitKaJKaNLuiCntzjLuNPw9I0BQ=', si)
    usr.save()
    # In addition to creating an account we will also generate keypair
    g = Random.new().read
    key = RSA.generate(2048, g)
    private = key.exportKey(format="PEM")
    public = key.publickey().exportKey(format="PEM")
    # And make a Reporter object that adds data to our User object
    reporter = Reporter(user=usr,publickey=public,privatekey=private)
    reporter.save()
    permission = Permission.objects.get(codename='add_report')
    usr.user_permissions.add(permission)

    # Make the site manager group
    sm = Group(name='Site Manager')
    sm.save()
    usr.groups.add(sm)
    usr.save()
    