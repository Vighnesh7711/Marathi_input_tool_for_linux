#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Installing Maza Marathi..."

# Create directory
mkdir -p /usr/share/maza-marathi/src
mkdir -p /usr/share/maza-marathi/icons

# Copy Source Code
cp -r ../src/* /usr/share/maza-marathi/src/
cp marathi_ibus.py /usr/share/maza-marathi/
touch /usr/share/maza-marathi/__init__.py

# Ensure executable
chmod +x /usr/share/maza-marathi/marathi_ibus.py

# Copy XML definition
cp maza-marathi.xml /usr/share/ibus/component/

echo "Installation complete."
echo "Please restart IBus ('ibus restart') and add 'Maza Marathi' from Settings > Region & Language."
