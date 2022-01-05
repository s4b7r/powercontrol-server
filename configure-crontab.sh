#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$(realpath "$0")")
. "$SCRIPT_PATH/venv/bin/activate"
python "$SCRIPT_PATH/configure-crontab.py"

chmod 0644 powercontrol-server-crontab
ln -s "$(pwd)/powercontrol-server-crontab" /etc/cron.d/powercontrol-server-crontab
crontab /etc/cron.d/powercontrol-server-crontab
