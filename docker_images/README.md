# How to use the content of this folder

This folder serves as storage for custom Docker images configuration.
Each sub folder corresponds to an image and comes with a bash script to build the image.

### Steps to follow

(Assuming your working directory is the 'docker_images' folder.)

> {sub_folder}/create_img.sh  -  This will build the image associated with the specified sub folder.

### Additional information

Please note that the dirty_cow image will not allow you to actually exploit a dirty_cow vulnerability.
This is due to the fact that this vulnerability is linked to specific versions of the Linux kernel and Docker containers run on top of your host machine kernel.
This means that unless your host machine kernel is vulnerable the vulnerability will not work as intended.