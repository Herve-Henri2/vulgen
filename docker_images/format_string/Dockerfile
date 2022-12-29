FROM ubuntu

WORKDIR /usr/app/src

COPY format_vuln.c ./
COPY flag.txt ./

RUN useradd -u 8877 appuser

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc-multilib && \
    apt-get -y install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential && \
    python3 -m pip install --upgrade pwntools && \
    rm -rf /var/lib/apt/lists/* && \
    gcc format_vuln.c -o format_vuln -fno-stack-protector -no-pie -m32 && \
    rm format_vuln.c && \
    chown root:root flag.txt && \
    chmod 600 flag.txt && \  
    chown root:root format_vuln && \
    chmod 4655 format_vuln


USER appuser