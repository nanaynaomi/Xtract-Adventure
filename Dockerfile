
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

# install the nvm binary
COPY install-nvm.sh /usr/sbin
SHELL ["/bin/bash", "--login", "-i", "-c"]
RUN dos2unix /usr/sbin/install-nvm.sh
RUN cat /usr/sbin/install-nvm.sh | bash
RUN source /root/.bashrc && nvm install 14.16.1
RUN npm install -g localtunnel
SHELL ["/bin/bash", "--login", "-c"]

RUN pip install slackclient slack_bolt Flask
RUN echo "alias python=python3" >> /root/.bashrc

COPY slackbot /slackbot
COPY Entrypoint.sh /usr/sbin
RUN dos2unix /usr/sbin/Entrypoint.sh

ENTRYPOINT ["/usr/sbin/Entrypoint.sh"]
