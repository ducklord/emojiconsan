FROM ubuntu:latest

ARG GIT_COMMIT=unknown
LABEL git-commit=$GIT_COMMIT

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates jq cron \
    && rm -rf /var/lib/apt/lists/*

COPY crontab /etc/cron.d/simple-cron
COPY ./emojiconsan.py /

RUN chmod 0644 /etc/cron.d/simple-cron

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh
