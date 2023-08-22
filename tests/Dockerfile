FROM ubuntu:20.04

RUN useradd -u 1001 -ms /bin/bash dockeruser

RUN set -x \
    && pythonVersions='python3.8 python3.9 python3.10 python3.11' \
    && apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && apt-add-repository ppa:/deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends $pythonVersions \
    && apt-get purge -y --auto-remove software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get -y install python3-pip
RUN pip3 install tox

USER dockeruser
WORKDIR /home/dockeruser

CMD bash