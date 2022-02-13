FROM ubuntu:latest

ARG GIT_COMMIT=unknown
LABEL git-commit=$GIT_COMMIT

RUN apt-get update \
    && apt-get install -y --no-install-recommends python pip ca-certificates cron \
    && rm -rf /var/lib/apt/lists/*

COPY crontab /etc/cron.d/simple-cron
COPY ./emojiconsan.py /
COPY ./requirements.txt /

RUN pip install -r requirements.txt

RUN chmod 0644 /etc/cron.d/simple-cron

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh
