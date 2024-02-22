#!/bin/bash

# Superuser check
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Create user and group if they do not exist
if ! id "bob" &>/dev/null; then
    useradd bob
fi

if ! getent group faculty &>/dev/null; then
    groupadd faculty
fi

# Create the required directory structure
mkdir -p /cs/home/stu/bob

# Set the directory permissions as per the document
chmod 755 /cs
chown root:root /cs

chmod 755 /cs/home
chown root:root /cs/home

chmod 755 /cs/home/stu
chown root:faculty /cs/home/stu

# The 'bob' directory needs special attention due to setgid bit
chmod 2750 /cs/home/stu/bob
chown bob:faculty /cs/home/stu/bob

# Navigate to Bob's home directory
cd /cs/home/stu/bob

# Create the files
touch data.txt secret.txt

# Set permissions for the files
chmod 640 data.txt
chown bob:faculty data.txt

chmod 640 secret.txt
chown bob:faculty secret.txt

echo "Setup complete. Directory and file permissions are set as per requirements."

# CLI Usage:
# sudo chmod +x setup_permissions.sh
# sudo ./setup_permissions.sh
