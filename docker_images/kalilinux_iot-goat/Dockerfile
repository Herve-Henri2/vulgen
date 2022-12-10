FROM kalilinux:custom

RUN apt-get install -y \
    unzip \
    gawk

WORKDIR /usr/app/src

COPY files/IoTGoat-raspberry-pi2.zip ./
COPY files/mirai-botnet.txt ./

RUN unzip IoTGoat-raspberry-pi2.zip
RUN rm IoTGoat-raspberry-pi2.zip

CMD ["/bin/bash"]