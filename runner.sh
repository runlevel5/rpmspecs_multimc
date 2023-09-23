#!/bin/sh
set -e
MMC_DATA_DIR="${XDG_DATA_HOME-"$HOME"/.local/share}/multimc"
exec /opt/multimc/bin/DevLauncher -d "$MMC_DATA_DIR" "$@"
