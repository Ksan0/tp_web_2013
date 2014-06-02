from django.conf.urls import patterns, include, url
from ask.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^signup$', signup),
    url(r'^signin$', signin),
    url(r'^signout$', signout),
    url(r'^ask$', ask),
    url(r'^user$', userinfo),
    url(r'^question$', question),
    url(r'^answer$', answer),
    url(r'^solved$', solved),
    url(r'^is_right$', is_right),
    url(r'^qvoice$', qvoice),
    url(r'^avoice$', avoice),
    url(r'^.*$', error404),
    # Examples:
    # url(r'^$', 'Project.views.home', name='home'),
    # url(r'^Project/', include('Project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
