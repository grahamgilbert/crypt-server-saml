import argparse
import subprocess
import os


# parser = argparse.ArgumentParser()
# parser.add_argument('tag', nargs='?', default='')
# args = parser.parse_args()

tag = os.getenv("TAG", "")

if tag == "":
    if os.getenv("CIRCLE_BRANCH") == "master":
        tag = "latest"
    else:
        tag = os.getenv("CIRCLE_BRANCH")

print(tag)
dockerfile_content = """FROM macadmins/crypt-server:{}

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

""".format(
    tag
)

with open("Dockerfile", "w") as dockerfile:
    dockerfile.write(dockerfile_content)

cmd = ["docker", "build", "-t", "macadmins/crypt-server-saml:{}".format(tag), "."]

print(subprocess.check_output(cmd))

cmd = [
    "docker",
    "login",
    "-u",
    "{}".format(os.getenv("DOCKER_USER")),
    "-p",
    "{}".format(os.getenv("DOCKER_PASS")),
]

try:
    print(subprocess.check_output(cmd))
except subprocess.CalledProcessError:
    print("Failed to login to docker")

cmd = ["docker", "push", "macadmins/crypt-server-saml:{}".format(tag)]

print(subprocess.check_output(cmd))
