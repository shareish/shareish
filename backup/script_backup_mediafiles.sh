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

Backuplog="/var/shareish/mediafiles/backup_mediafiles.log"
BackupTime=$(date '+%Y-%m-%d_%H-%M')
BackupOutDir="/backup/shareish_mediafiles"
SourceDirectory="/backup/mediafiles"
BackupFileName="backup_mediafiles${BackupTime}.tar.gz"
BackupFilePath="${BackupOutDir}/${BackupFileName}"

mkdir -p ${BackupOutDir}



cho "Starting Backup of mediafiles Prod  at : ${BackupTime}"             > ${Backuplog}
echo "================================================================"         >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
touch ${BackupFilePath}
chmod a+rw ${BackupFilePath}
echo "tar -cf "$BackupFilePath" -C "$SourceDirectory" ."						>> ${Backuplog}
tar -czf "$BackupFilePath" -C "$SourceDirectory" .
echo "Removing  mediafiles backup files older than 7 days ..."                   >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
find ${BackupOutDir} -name *.tar.gz -ctime +7 -exec rm -f -v {} \;  |\
 sed -e "s/^removed/  removed/g"                                                >> ${Backuplog} 2>&1
echo ""                                                                         >> ${Backuplog}
echo "Following backup files left in ${BackupOutDir} ..."                          >> ${Backuplog}
echo ""                                                                         >> ${Backuplog}
ls -1t ${BackupOutDir} | sed -e "s/^PROD/  PROD/g"                                 >> ${Backuplog}


if [ $? -eq 0 ]; then															
    echo "La sauvegarde a été créée avec succès : $BackupOutDir/$BackupFileName" >> ${Backuplog}
else																			
    echo "Erreur : La sauvegarde a échoué."										>> ${Backuplog}
fi