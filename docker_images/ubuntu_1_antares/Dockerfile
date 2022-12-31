FROM ubuntu20-python-c:custom

RUN useradd -ms /bin/bash diego 
RUN ufw allow 22 
RUN ufw reload 

USER diego
WORKDIR /home/diego

COPY files ./

EXPOSE 22
