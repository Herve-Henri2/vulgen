FROM ubuntu20-python-c:20.04-3.8

WORKDIR /usr/app/src

COPY main.py ./
COPY stack0.c ./
COPY payload.txt ./

RUN gcc -std=c99 -fno-stack-protector -g stack0.c -o stack0

CMD ["python3.8", "./main.py"]
