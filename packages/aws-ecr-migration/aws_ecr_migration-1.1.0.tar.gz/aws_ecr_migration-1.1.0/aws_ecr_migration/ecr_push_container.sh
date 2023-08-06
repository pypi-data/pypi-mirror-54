#!/usr/bin/env bash

set -e

CONTAINER=$1
REPOSITORY=$2

docker commit ${CONTAINER} ${REPOSITORY}
docker push ${REPOSITORY}
