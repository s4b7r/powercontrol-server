#!/usr/bin/env bash

apt update
apt -y install etherwake
sed -i "s;ETHERWAKE_PATH;$(dirname "$(which etherwake)");g" wake.sh

echo "Creating Python environment will usually take some time..."
python3 -m venv venv

SCRIPT_PATH=$(dirname "$(realpath "$0")")
. "$SCRIPT_PATH/venv/bin/activate"

pip3 install -r requirements.txt

chmod u+x powercontrol-server.sh

ufw allow in 8000/tcp

ln -s "$(pwd)/powercontrol-server.service" /etc/systemd/system/powercontrol-server.service
sed -i "s;INSTALL_DIR;$(pwd);g" powercontrol-server.service
systemctl daemon-reload
systemctl start powercontrol-server.service

chmod u+x wake.sh

python "$SCRIPT_PATH/configure-crontab.py"

chmod 0644 powercontrol-server-crontab
ln -s "$(pwd)/powercontrol-server-crontab" /etc/cron.d/powercontrol-server-crontab
