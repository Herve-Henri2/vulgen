FROM ubuntu20-python-c:20.04-3.8

WORKDIR /usr/app/src

COPY files/main.py ./
COPY files/overflow.c ./
COPY files/payload.txt ./

RUN gcc -g overflow.c -o overflow

CMD ["python3.8", "./main.py"]
