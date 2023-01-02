FROM ubuntu20-python-c:custom

RUN useradd -ms /bin/bash diego 
RUN service ssh start

USER diego
WORKDIR /home/diego

COPY files ./

EXPOSE 22
