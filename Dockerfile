FROM macadmins/crypt-server:latest
MAINTAINER Graham Gilbert <graham@grahamgilbert.com>
ENV DJANGO_SAML_VERSION 0.16.11

RUN apt-get update && apt-get install -y libxmlsec1-dev libxml2-dev xmlsec1 \
    && pip install djangosaml2==$DJANGO_SAML_VERSION

ADD attributemaps /home/app/crypt/fvserver/attributemaps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
ADD urls.py /home/app/crypt/fvserver/urls.py
