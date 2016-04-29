FROM macadmins/crypt-server:2.0.1
MAINTAINER Graham Gilbert <graham@grahamgilbert.com>
ENV DJANGO_SAML_VERSION 0.14.4

RUN apt-get update && apt-get install -y python-setuptools python-dev libxmlsec1-dev libxml2-dev xmlsec1 \
    && easy_install pip \
    && pip install djangosaml2==$DJANGO_SAML_VERSION
# ADD settings.py /home/app/sal/sal/settings.py
# ADD run-dev.sh /run-dev.sh
ADD attribute-maps /home/app/crypt/fvserver/attribute-maps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
ADD urls.py /home/app/crypt/fvserver/urls.py
#RUN python /home/app/crypt/manage.py makemigrations
