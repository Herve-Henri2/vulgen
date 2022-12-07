FROM kalilinux:custom

RUN apt-get install -y \
    unzip \
    gawk

WORKDIR /usr/app/src

COPY files/IoTGoat-filesystem.zip ./
COPY files/mirai-botnet.txt ./

RUN mkdir IoTGoat-filesystem
RUN unzip IoTGoat-filesystem.zip -d IoTGoat-filesystem

CMD ["/bin/bash"]