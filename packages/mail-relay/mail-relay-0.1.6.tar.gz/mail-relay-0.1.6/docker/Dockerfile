FROM python:2.7.16

RUN addgroup --gid 10000 relay && \
    adduser --uid 10000 \
            --disabled-password \
            --home /home/relay \
            --gid 10000 relay

RUN apt-get update -y \
    && apt-get install -y libsodium-dev \
    && apt-get clean


WORKDIR /home/relay

ARG VERSION
RUN pip download mail-relay==${VERSION} -d .
RUN tar zxvf mail-relay-${VERSION}.tar.gz
RUN chown -R relay:relay /home/relay

USER relay

RUN cd mail-relay-${VERSION} && \
    pip install --user -r requirements.txt -r requirements_linux.txt && \
    pip install --user . && \
    /home/relay/.local/bin/relay --help

ENTRYPOINT [ "/home/relay/.local/bin/relay" ]
CMD [ "info" ]
