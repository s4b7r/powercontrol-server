#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$(realpath "$0")")
. "$SCRIPT_PATH/venv/bin/activate"
python "$SCRIPT_PATH/powercontrol-server.py"