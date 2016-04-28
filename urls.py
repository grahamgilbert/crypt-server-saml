from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from origurls import *

urlpatterns += patterns('',

    (r'^saml2/', include('djangosaml2.urls')),
)
