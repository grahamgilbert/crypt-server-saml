import argparse
import subprocess
import os


# parser = argparse.ArgumentParser()
# parser.add_argument('tag', nargs='?', default='')
# args = parser.parse_args()

tag = os.getenv('TAG', '')

if tag == '':
    if os.getenv('CIRCLE_BRANCH') == 'master':
        tag = 'latest'
    else:
        tag = os.getenv('CIRCLE_BRANCH')

print(tag)
dockerfile_content = """FROM macadmins/crypt-server:{}
MAINTAINER Graham Gilbert <graham@grahamgilbert.com>
ENV DJANGO_SAML_VERSION 0.16.11

RUN apk add --no-cache --virtual .build-deps \
    xmlsec-dev xmlsec git gcc libc-dev \
    && pip install --no-cache-dir --upgrade setuptools \
    && pip install --no-cache-dir git+git://github.com/francoisfreitag/djangosaml2.git@613356c7f0e18ecfde07e4d282d0b82b0f4f7268 \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, \"\nso:", $2); print \"so:\" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

COPY attributemaps /home/app/crypt/fvserver/attributemaps
RUN mv /home/app/crypt/fvserver/urls.py /home/app/crypt/fvserver/origurls.py
COPY urls.py /home/app/crypt/fvserver/urls.py

""".format(tag)

with open("Dockerfile", "w") as dockerfile:
    dockerfile.write(dockerfile_content)

cmd = [
    'docker',
    'build',
    '-t',
    'macadmins/sal-saml:{}'.format(tag),
    '.'
]

print(subprocess.check_output(cmd))

cmd = [
    'docker',
    'login',
    '-u',
    '{}'.format(os.getenv('DOCKER_USER')),
    '-p',
    '{}'.format(os.getenv('DOCKER_PASS'))
]

try:
    print(subprocess.check_output(cmd))
except subprocess.CalledProcessError:
    print('Failed to login to docker')

cmd = [
    'docker',
    'push',
    'macadmins/sal-saml:{}'.format(tag)
]

print(subprocess.check_output(cmd))
