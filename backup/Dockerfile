FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add PostgreSQL repository
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


RUN apt-get update && apt-get install -y \
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

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

ENV POSTGRES_CONTAINER=db
ENV POSTGRES_DB=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432
