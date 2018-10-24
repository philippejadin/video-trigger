#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi


echo "Installing hello_video..."
echo "========================="
git clone https://github.com/adafruit/pi_hello_video.git
cd pi_hello_video
./rebuild.sh
cd hello_video
make install
cd ../..
rm -rf pi_hello_video



echo "Copy config file..."
echo "=========================="
cp video_trigger.ini /boot/video_trigger.ini


echo "Add to systemd"
echo "=========================="
cp video_trigger.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable video_trigger.service

# enable logs
mkdir -p /var/log/journal
