#!/bin/bash

#
# Copyright (c) 2009-2017. Authors: see NOTICE file.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



mkdir -p /var/shareish/
mkdir -p /var/shareish/mediafiles

cp /tmp/script_backup_postgres.sh /var/shareish/script_backup.sh
cp /tmp/script_backup_mediafiles.sh /var/shareish/mediafiles/script_backup_mediafiles.sh
	

chmod +x /var/shareish/script_backup.sh
chmod +x /var/shareish/mediafiles/script_backup_mediafiles.sh




#hostname:port:database:username:password
echo "$POSTGRES_CONTAINER:$POSTGRES_PORT:$POSTGRES_DB:$POSTGRES_USER:$POSTGRES_PASSWORD" > /root/.pgpass
cat /root/.pgpass
chmod 600 /root/.pgpass

echo "Add the backup script to crontab"
touch /tmp/crontab
echo "#Setting env var" >> /tmp/crontab

echo "DATABASE=postgres" >> /tmp/crontab
echo "USER=postgres" >> /tmp/crontab


echo "CONTAINER=db" >> /tmp/crontab
echo "#End setting env var" >> /tmp/crontab

echo "30 23 * * * /var/shareish/script_backup.sh postgres" >> /tmp/crontab
echo "30 23 * * * /var/shareish/mediafiles/script_backup_mediafiles.sh" >> /tmp/crontab
crontab /tmp/crontab
rm /tmp/crontab

service rsyslog restart
service cron restart

touch /var/shareish/backup_database.log
touch /var/shareish/mediafiles/backup_mediafiles.log
tail -f /var/shareish/backup_database.log
tail -f var/shareish/mediafiles/backup_mediafiles.log


