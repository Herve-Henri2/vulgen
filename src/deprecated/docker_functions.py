import docker

def get_image_name(image_tag):
        image_tag=str(image_tag)
        return image_tag.replace("<bound method Image.tag of <Image: '", '').replace("'>>", '').replace("<Image: '",'').replace("'>", '')

def image_in(images, wanted_image_name):
    '''
    Checks whether or not an image list contains a specific image.
    '''
    for image in images:
        image_name = get_image_name(image.tag)
        if wanted_image_name in image_name:
            return True
    return False

def container_in(containers, wanted_container_image_name):
    '''
    Checks whether or not a container list contains a specific container based on the container's image name.
    '''
    for container in containers:
        container_image_name = get_image_name(container.image)
        if wanted_container_image_name in container_image_name:
            return True
    return False

def get_image(images, image_name):
    '''
    Searches for an image in an image list based on the image's name.

    Returns: docker.image object
    '''
    if not image_in(images, image_name):
        #print(f"There is no image corresponding to {image_name}")
        return
    for index, image in enumerate(images):
        if image_name in get_image_name(image.tag):
            return image, index

def get_container(containers, container_image_name):
    '''
    Searches for a container object in a container list based on the container's image name.

    Returns: docker.container object
    '''
    if not container_in(containers, container_image_name):
        #print(f"No {container_image_name} container was found")
        return
    for index, container in enumerate(containers):
        if container_image_name in get_image_name(container.image):
            return container, index

def StartContainer(self):
    selection = self.table_view.selectedItems()
    id = selection[0].text()
    command = f"docker start -i {id}"
    misc.open_terminal(configuration['operating_system'], command=command)