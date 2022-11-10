FROM macadmins/crypt-server:latest

RUN apk add --no-cache --virtual .build-deps \
    xmlsec-dev xmlsec git gcc libc-dev libpq \
    && pip install --no-cache-dir --upgrade setuptools \
    && pip install djangosaml2==1.5.3

COPY attributemaps /home/app/crypt/fvserver/attributemaps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
COPY urls.py /home/app/crypt/fvserver/urls.py
COPY __init__.py /home/app/crypt/server/__init__.py
COPY apps.py /home/app/crypt/server/apps.py
COPY signals.py /home/app/crypt/server/signals.py
