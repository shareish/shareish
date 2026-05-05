FROM ubuntu:22.04


RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    lsb-release \
    build-essential \
    locate \
    net-tools \
    cron \
    rsyslog \
    gzip \
    postgresql-client-14 \
    && rm -rf /var/lib/apt/lists/*

COPY script_backup_postgres.sh /tmp/script_backup_postgres.sh
COPY script_backup_mediafiles.sh /tmp/script_backup_mediafiles.sh
COPY deploy.sh /tmp/deploy.sh

RUN chmod +x /tmp/deploy.sh

ENTRYPOINT ["/tmp/deploy.sh"]

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

EXPOSE 5432

