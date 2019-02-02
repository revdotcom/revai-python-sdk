FROM ubuntu:18.04

RUN useradd -u 1001 -ms /bin/bash dockeruser

RUN set -x \
    && pythonVersions='python2.7 python3.4 python3.5 python3.6 python3.7' \
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