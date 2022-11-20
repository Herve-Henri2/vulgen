FROM xenial-python-c:xenial-3.5

WORKDIR /usr/app/src

COPY files/main.py ./
COPY files/dirtycow.c ./

CMD ["python3.5", "./main.py"]