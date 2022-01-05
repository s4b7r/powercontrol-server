#!/usr/bin/env bash

exec 1> >(logger -p user.info -t powercontrol-server-wake) 2>&1
echo "Waking $1"
etherwake $1
echo "Woke (hopefully) $1"
