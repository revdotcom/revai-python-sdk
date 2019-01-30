FROM ubuntu:18.04

RUN apt update

RUN set -x \
    && pythonVersions='python2.7 python3.4 python3.5 python3.6 python3.7' \
    && apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && apt-get update \
    && apt-get install -y --no-install-recommends $pythonVersions \
    && apt-get purge -y --auto-remove software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install python-pip

CMD bash