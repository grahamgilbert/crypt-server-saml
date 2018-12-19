from django.urls import path, include

from .origurls import *

urlpatterns += [path("saml2/", include("djangosaml2.urls"))]
