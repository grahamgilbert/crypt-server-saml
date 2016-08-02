from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from origurls import *

urlpatterns += [

    url(r'^saml2/', include('djangosaml2.urls')),
]
