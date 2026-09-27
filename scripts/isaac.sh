#!/usr/bin/env bash
set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./scripts/isaac.sh <python_script> [args...]"
    exit 1
fi

SCRIPT="$(wslpath -w "$1")"
shift

cmd.exe /C C:\\isaac-sim\\python.bat "$SCRIPT" "$@"
