
# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi


echo "Add to systemd and enable"
echo "=========================="
cp video-trigger.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable video-trigger.service
