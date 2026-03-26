FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PG_VERSION=14


RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    wget \
    && . /etc/os-release \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ ${VERSION_CODENAME}-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt/ ${VERSION_CODENAME}-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    locate \
    net-tools \
    cron \
    rsyslog \
    gzip \
    postgresql-client-$PG_VERSION \
    && apt-get purge -y --auto-remove wget gnupg \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY script_backup_postgres.sh script_backup_mediafiles.sh deploy.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

EXPOSE 5432

ENTRYPOINT ["deploy.sh"]