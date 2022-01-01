#!/bin/sh
chmod 0644 /etc/cron.d/pwrctrl-srv
crontab /etc/cron.d/pwrctrl-srv
