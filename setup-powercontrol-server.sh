#!/usr/bin/env bash

apt update
apt -y install etherwake

python3 -m venv venv
source venv/bin/activate
pip3 install starlette uvicorn

chmod u+x run-powercontrol-server.sh

ufw allow in 8000/tcp

ln -s "$(pwd)/powercontrol-server.service" /etc/systemd/system/powercontrol-server.service
sed -i "s;INSTALL_DIR;$(pwd);g" powercontrol-server.service
systemctl daemon-reload
systemctl start powercontrol-server.service

chmod u+x configure-crontab.sh
configure-crontab.sh
