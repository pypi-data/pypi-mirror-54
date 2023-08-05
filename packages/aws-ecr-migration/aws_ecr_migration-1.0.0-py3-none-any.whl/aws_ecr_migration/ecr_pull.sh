#!/usr/bin/env bash

set -e

REPOSITORY=$1

docker pull ${REPOSITORY}
