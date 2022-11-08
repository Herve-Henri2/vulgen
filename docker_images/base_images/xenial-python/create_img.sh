#! /usr/bin/bash

# Create the new image
docker image build -t xenial-python:xenial-3.5 base_images/xenial-python
