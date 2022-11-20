FROM ubuntu20-python-c

WORKDIR /usr/app/src

COPY files/instructions.txt ./
COPY files/stack0.c ./
COPY files/payload.txt ./

RUN gcc -std=c99 -fno-stack-protector -g stack0.c -o stack0

CMD ["/bin/bash"]
