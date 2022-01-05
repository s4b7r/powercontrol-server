#!/usr/bin/env bash

apt update
apt -y install etherwake

python3 -m venv venv
source venv/bin/activate
pip3 install starlette uvicorn

chmod u+x run-powercontrol-server.sh

ln -s "$(pwd)/powercontrol-server.service" /etc/systemd/system/powercontrol-server.service
sed -i "s;INSTALL_DIR;$(pwd);g" powercontrol-server.service
systemctl daemon-reload

echo "Configure your timeframes.json and execute configure-crontab.sh."
echo "Then do 'systemctl start powercontrol-server.service'"
