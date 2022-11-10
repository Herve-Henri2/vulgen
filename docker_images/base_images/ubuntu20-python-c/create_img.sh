#! /usr/bin/bash

# Retrieve this script directory
DIR_NAME=$(dirname ${BASH_SOURCE:-$0})

# Create the new image
docker image build -t ubuntu20-python-c:20.04-3.8 $DIR_NAME
