#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install_production.sh"
  exit 1
fi


cd /tmp
wget https://raw.githubusercontent.com/janztec/empc-arpi-linux-readonly/master/install-experimental.sh -O install-experimental.sh
sudo bash install-experimental.sh
