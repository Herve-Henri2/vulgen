FROM ubuntu20-python-c:20.04-3.8

WORKDIR /usr/app/src

COPY files/main.py ./
COPY files/stack0.c ./
COPY files/payload.txt ./

RUN gcc -std=c99 -fno-stack-protector -g stack0.c -o stack0

CMD ["python3.8", "./main.py"]
