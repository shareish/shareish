# On utilise l'image officielle qui contient déjà postgresql-client-14
FROM postgres:14

# Empêche les questions interactives
ENV DEBIAN_FRONTEND=noninteractive

# On installe les outils système via les dépôts standards (plus fiables)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cron \
    gzip \
    net-tools \
    rsyslog \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copie de vos scripts
COPY script_backup_postgres.sh /tmp/script_backup_postgres.sh
COPY script_backup_mediafiles.sh /tmp/script_backup_mediafiles.sh
COPY deploy.sh /tmp/deploy.sh

# Permissions
RUN chmod +x /tmp/deploy.sh /tmp/script_backup_postgres.sh /tmp/script_backup_mediafiles.sh

ENTRYPOINT ["/tmp/deploy.sh"]