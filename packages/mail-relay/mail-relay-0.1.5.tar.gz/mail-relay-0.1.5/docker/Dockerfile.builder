# syntax=docker/dockerfile:experimental

FROM python:2.7.16


RUN addgroup --gid 10000 builder && \
    adduser --uid 10000 \
            --disabled-password \
            --home /home/builder \
            --gid 10000 builder

RUN apt-get update -y \
    && apt-get install -y libsodium-dev \
    && apt-get clean

RUN pip install tox

WORKDIR /home/builder
COPY . ./mail-relay

WORKDIR /home/builder/mail-relay

CMD ["/bin/bash"]
