#!/bin/sh

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./disable.sh"
  exit 1
fi

# Disable any supervisor process that start video trigger.
supervisorctl stop video_trigger
mv /etc/supervisor/conf.d/video_trigger.conf /etc/supervisor/conf.d/video_trigger.conf.disabled
