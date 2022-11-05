#! /usr/bin/bash

# Create the required image if not already done
ubuntu20-python-c/create_img.sh

# Delete all containers
docker rm $(docker ps -a -q)

# Retrieve id of old image
old_img=$(docker images | grep buffer_overflow)
echo -e ${old_img// /'\n'} > tmp1.txt

echo -e $(docker images -q) > tmp2.txt
ids=$(cat tmp2.txt)
echo -e ${ids// /'\n'} > tmp2.txt

id=$(grep -Fxf tmp1.txt tmp2.txt)

rm tmp1.txt tmp2.txt

# Delete old image
docker rmi $id

# Create the new image
docker image build -t buffer_overflow:latest buffer_overflow

# Run the new image
#clear
#docker run -it python_test:latest
