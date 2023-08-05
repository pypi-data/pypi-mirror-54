#!/usr/bin/env bash

set -e

IMAGE=$1
REPOSITORY=$2

docker tag ${IMAGE} ${REPOSITORY}
docker push ${REPOSITORY}
