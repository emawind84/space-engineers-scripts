#!/bin/bash

SCRIPT_BASE_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SCRIPT_NAME="${0##*/}"

export PATH=/home/pi/jupyter/env/bin:$PATH

set -e

#echo "Script name: [$SCRIPT_NAME]"
#echo "Base path: [$SCRIPT_BASE_PATH]"

cd $SCRIPT_BASE_PATH

python check_server.py "$@"
