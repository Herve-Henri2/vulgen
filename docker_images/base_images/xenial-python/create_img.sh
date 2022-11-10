#! /usr/bin/bash

# Retrieve this script directory
DIR_NAME=$(dirname ${BASH_SOURCE:-$0})

# Create the new image
docker image build -t xenial-python:xenial-3.5 $DIR_NAME
