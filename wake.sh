#!/usr/bin/env bash

exec 1> >(logger -p user.info -t powercontrol-server-wake) 2>&1
export PATH=ETHERWAKE_PATH
echo "Waking $1"
etherwake $1
echo "Woke (hopefully) $1"
