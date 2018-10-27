#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi

echo "Install packages"
apt install git python-pip python-pygame
pip install pyserial

echo "Setup automount of media stick"
echo LABEL=MEDIA /media/pi/MEDIA vfat32 defaults 0 0 >> /etc/fstab
mkdir -p /media/pi/MEDIA

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




# enable logs
echo "Enable persistent logs..."
echo "=========================="
mkdir -p /var/log/journal
