#!/bin/sh

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./disable.sh"
  exit 1
fi

echo "Configuring video_trigger to run on start..."
echo "==========================================="
cp video_trigger.conf /etc/supervisor/conf.d/
service supervisor restart
