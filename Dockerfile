FROM macadmins/crypt-server:2.2.0
MAINTAINER Graham Gilbert <graham@grahamgilbert.com>
ENV DJANGO_SAML_VERSION 0.15.0

RUN apt-get update && apt-get install -y python-setuptools python-dev libxmlsec1-dev libxml2-dev xmlsec1 \
    && easy_install pip \
    && pip install djangosaml2==$DJANGO_SAML_VERSION

ADD attributemaps /home/app/crypt/fvserver/attributemaps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
ADD urls.py /home/app/crypt/fvserver/urls.py
