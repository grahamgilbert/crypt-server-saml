#!/bin/bash
source SAL_ENVS

if [ "$1" != "" ]; then
    TAG="$1"
else
    TAG="latest"
fi

if [ "$2" != "" ]; then
    BRANCH="$2"
else
    BRANCH="master"
fi

URL="https://circleci.com/api/v1.1/project/github/salopensource/sal-saml/tree/${BRANCH}"
echo $TAG
jq -n '{build_parameters: {TAG: "$TAG"}}' | curl -X POST -d @- \
  --user ${CIRCLE_API_USER_TOKEN}: \
  --url $URL \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'