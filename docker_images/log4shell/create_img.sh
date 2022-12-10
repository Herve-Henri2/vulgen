#! /bin/bash

# Retrieve this script directory
DIR_NAME=$(dirname ${BASH_SOURCE:-$0})

# Delete all containers
#docker rm $(docker ps -a -q)

# Retrieve id of old image
old_img=$(docker images | grep $DIR_NAME)
echo -e ${old_img// /'\n'} > tmp1.txt

echo -e $(docker images -q) > tmp2.txt
ids=$(cat tmp2.txt)
echo -e ${ids// /'\n'} > tmp2.txt

id=$(grep -Fxf tmp1.txt tmp2.txt)

rm tmp1.txt tmp2.txt

# Delete old image
docker rmi -f $id

# Create the new image
docker image build -t $DIR_NAME:custom $DIR_NAME
