FROM ubuntu20-qemu:custom

WORKDIR /usr/app/src

COPY files/IoTGoat-x86.vmdk ./

CMD ["qemu-system-x86_64", "-hda", "IoTGoat-x86.vmdk", "-nographic", "-nic", "user,hostfwd=tcp::8022-:22"]