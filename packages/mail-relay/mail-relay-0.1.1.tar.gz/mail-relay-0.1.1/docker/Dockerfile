# syntax=docker/dockerfile:experimental

FROM python:2.7.16


RUN addgroup --gid 10000 preveil && \
    adduser --uid 10000 \
            --disabled-password \
            --home /home/preveil \
            --gid 10000 preveil

RUN apt-get update -y \
    && apt-get install -y libsodium-dev \
    && apt-get clean

RUN pip install tox

WORKDIR /home/preveil
COPY . ./mail-relay

WORKDIR /home/preveil/mail-relay

CMD ["/bin/bash"]
