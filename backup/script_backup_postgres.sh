#! /bin/bash

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


Backuplog="/var/shareish/backup_database.log"
BackupDatabase=$DATABASE
BackupTime=`date '+%Y-%m-%d_%H-%M'`
BackupOutDir="/backup/shareish_database/$BackupDatabase"
BackupFile="$BackupOutDir/PRODbackup-$BackupDatabase-$BackupTime.sql"

mkdir -p ${BackupOutDir}

echo "Starting Backup of Shareish Prod DB at : ${BackupTime}"             > ${Backuplog}
echo "================================================================"         >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
echo "Starting pg_dump to ${BackupFile} ..."                                    >> ${Backuplog}
touch ${BackupFile}
chmod a+rw ${BackupFile}
echo "pg_dump -h db -U postgres -w -f ${BackupFile} $BackupDatabase"        >> ${Backuplog} 2>&1
pg_dump -h db -U postgres -w -f ${BackupFile} $BackupDatabase               >> ${Backuplog} 2>&1      
PGDumpRC=$?
echo "  EXIT_CODE:${PGDumpRC}"                                                  >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
echo "Removing backup files older than 7 days ..."                              >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
find ${BackupOutDir} -name *.sql -ctime +7 -exec rm -f -v {} \;  |\
 sed -e "s/^removed/  removed/g"                                                >> ${Backuplog} 2>&1
echo ""                                                                         >> ${Backuplog}
echo "Following backup files left in ${BackupOutDir} ..."                          >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
ls -1t ${BackupOutDir} | sed -e "s/^PROD/  PROD/g"                                 >> ${Backuplog}




if [ $PGDumpRC -gt 0 ]
then
    echo "ERROR: Backup of ${BackupDatabase} failed. See ${Backuplog} for details."  >> ${Backuplog}

else
     echo "Backup of ${BackupDatabase} DB successful." >> ${Backuplog}
fi


   