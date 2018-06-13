
FROM ubuntu:14.04

WORKDIR /opt/pydocker/docker_py27

ADD . /opt/pydocker/docker_py27

MAINTAINER Leo Chao, bullet00067@gmail.com

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean


CMD ["bash"]
