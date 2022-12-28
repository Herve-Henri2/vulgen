FROM skysider/pwndocker

WORKDIR /usr/app/src

COPY format_vuln.c ./
COPY flag.txt ./

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc-multilib && \
    apt-get install -y python && \
    rm -rf /var/lib/apt/lists/* && \
    gcc format_vuln.c -o format_vuln -fno-stack-protector -no-pie -m32 && \
    rm format_vuln.c && \
    chown root:root flag.txt && \
    chmod 600 flag.txt && \  
    chown root:root format_vuln && \
    chmod 4655 format_vuln &&