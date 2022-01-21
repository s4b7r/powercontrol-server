#!/usr/bin/env bash

rm -r /var/backups/powercontrol-server/preupdate-backup
mkdir -p /var/backups/powercontrol-server/preupdate-backup
cp timeframes.json /var/backups/powercontrol-server/preupdate-backup/

rm /etc/cron.d/powercontrol-server-crontab
rm powercontrol-server-crontab

systemctl disable powercontrol-server.service
systemctl stop powercontrol-server.service
rm /etc/systemd/system/powercontrol-server.service
rm powercontrol-server.service
systemctl daemon-reload

ufw delete allow in 8000/tcp

rm -rf venv

rm wake.sh

git fetch -a
git reset --hard origin/main

cp /var/backups/powercontrol-server/preupdate-backup/* ./

. setup-powercontrol-server.sh
