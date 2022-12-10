#! /bin/bash

# Retrieve this script directory
DIR_NAME=$(dirname ${BASH_SOURCE:-$0})

# Create the new image
docker image build -t kalilinux:custom $DIR_NAME

