postgresql-client-14
FROM postgres:14


ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cron \
    gzip \
    net-tools \
    rsyslog \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


COPY script_backup_postgres.sh /tmp/script_backup_postgres.sh
COPY script_backup_mediafiles.sh /tmp/script_backup_mediafiles.sh
COPY deploy.sh /tmp/deploy.sh

RUN chmod +x /tmp/deploy.sh /tmp/script_backup_postgres.sh /tmp/script_backup_mediafiles.sh

ENTRYPOINT ["/tmp/deploy.sh"]