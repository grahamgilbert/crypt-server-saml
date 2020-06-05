FROM macadmins/crypt-server:latest
MAINTAINER Graham Gilbert <graham@grahamgilbert.com>
ENV DJANGO_SAML_VERSION 0.16.11

RUN apk add --no-cache --virtual .build-deps \
    xmlsec-dev xmlsec git gcc libc-dev \
    && pip install --no-cache-dir --upgrade setuptools \
    && pip install --no-cache-dir git+git://github.com/knaperek/djangosaml2.git@ef59c7c7096ee32e6ce75ef42af7c01639dc6dbc
# \
# && runDeps="$( \
#         scanelf --needed --nobanner --recursive /venv \
#                 | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#                 | sort -u \
#                 | xargs -r apk info --installed \
#                 | sort -u \
# )" \
# && apk add --virtual .python-rundeps $runDeps \
# && apk del .build-deps

COPY attributemaps /home/app/crypt/fvserver/attributemaps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
COPY urls.py /home/app/crypt/fvserver/urls.py
COPY __init__.py /home/app/crypt/server/__init__.py
COPY apps.py /home/app/crypt/server/apps.py
COPY signals.py /home/app/crypt/server/signals.py
