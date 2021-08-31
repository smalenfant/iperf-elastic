FROM alpine:latest

MAINTAINER Steve Malenfant <steve.malenfant@cox.com>

RUN apk --update add \
    iperf3 \
    jq \
    curl \
    python3 \
    py3-pip \
    ca-certificates \
    && rm -rf /var/cache/apk/* \
    && adduser -S iperf

RUN pip3 install elasticsearch

USER iperf

# Expose server if ran...
EXPOSE 5201

COPY run-iperf.py /tmp/run-iperf.py

ENTRYPOINT ["/tmp/run-iperf.py"]

# iperf -s = run in Server mode
#CMD ["-s"]
