#!/bin/bash

# File name: setup_assignment.sh
# Author: Abraham Reines
# Date: February 21, 2024

# This script complies with the requirements. Should produce output consistent with assignment when executed in appropriate environment.

usermod -a -G faculty bob

gpasswd -d bob bobsgroup &>/dev/null

usermod -a -G csmajor alice
usermod -a -G csmajor bob

# Set up the directory permissions
chmod 755 /cs
chmod 755 /cs/home
chmod 2755 /cs/home/stu

chown bob:faculty /cs/home/stu/bob
chmod 2750 /cs/home/stu/bob

touch /cs/home/stu/bob/data.txt
touch /cs/home/stu/bob/secret.txt
chown bob:faculty /cs/home/stu/bob/data.txt
chown bob:faculty /cs/home/stu/bob/secret.txt
chmod 644 /cs/home/stu/bob/data.txt
chmod 600 /cs/home/stu/bob/secret.txt

setfacl -m u:alice:r-- /cs/home/stu/bob/data.txt

echo "Initial Permissions:"
echo "--------------------------------"
echo "Directory permissions:"
ls -ld /cs /cs/home /cs/home/stu /cs/home/stu/bob
echo "--------------------------------"
echo "File permissions in Bob's home directory:"
ls -l /cs/home/stu/bob/data.txt /cs/home/stu/bob/secret.txt
echo "--------------------------------"
echo "ACL for data.txt:"
getfacl /cs/home/stu/bob/data.txt
echo "--------------------------------"
echo "Current users and groups:"
groups bob
groups alice
echo "--------------------------------"
echo "Setup complete. Users, groups, permissions, and ACL are all set as per the assignment scenario."