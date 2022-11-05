FROM ubuntu20-python-c:20.04-3.8

WORKDIR /usr/app/src

COPY main.py ./
COPY overflow.c ./
COPY payload.txt ./

RUN gcc -g overflow.c -o overflow

CMD ["python3.8", "./main.py"]
