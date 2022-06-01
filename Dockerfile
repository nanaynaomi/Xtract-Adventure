
FROM ubuntu:jammy

EXPOSE 3000

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y \
    apt \
    bash \
    vim \
    curl \
    dos2unix \
    python3 python3-venv python3-pip \ 
    && rm -rf /var/lib/apt/lists/*

RUN pip install slackclient slack_bolt Flask
RUN echo "alias python=python3" >> /root/.bashrc

COPY slackbot /slackbot
COPY Entrypoint.sh /usr/sbin
RUN dos2unix /usr/sbin/Entrypoint.sh

ENTRYPOINT ["/usr/sbin/Entrypoint.sh"]
