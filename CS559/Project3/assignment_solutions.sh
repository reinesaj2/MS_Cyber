#!/bin/bash

# File name: assignment_solutions_v2.sh
# Author: Abraham Reines
# Date: February 21, 2024
# Modified: February 22, 2024

# check read permission for Alice
Can_she_read?() {
  if [ -r "$1" ]; then
    # If file is readable, check if the 'alice' user is owner or part of group with read permission.
    owner=$(ls -l "$1" | awk '{print $3}')
    group=$(ls -l "$1" | awk '{print $4}')
    if [ "$owner" == "alice" ] || [ "$group" == "csmajor" ] || [ "$(ls -l "$1" | cut -c8)" == "r" ]; then
      echo "yes - Alice can read the file $1 because the 'others' permissions on the file allow read access."
    else
      echo "no - Alice cannot read the file $1 because she lacks read permissions."
    fi
  else
    echo "no - Alice cannot read the file $1 because the file does not exist or is not readable."
  fi
}

# check remove permission for Alice
Can_she_remove?() {
  if sudo -u alice test -w "$1"; then
    echo "yes - Alice can remove the file $1 because she has write permissions."
  else
    echo "no - Alice cannot remove the file $1 because she lacks write permissions."
  fi
}

# simulate the creation of a new file by Bob with specific permissions
Bobs_new_file() {
  sudo -u bob touch "$1"
  sudo -u bob chmod g+s "$1"
  echo "My Super Secret is b7sd78shes" > mysecret2.txt
  echo "The full permissions for the new file $1 are:"
  ls -l "$1"
}
echo
echo "3.4.1 Solutions:"
echo "--------------------------------"
# Check permissions for Alice
echo "Question 1:"
Can_she_read? "/cs/home/stu/bob/data.txt"

echo "Question 2:"
Can_she_remove? "/cs/home/stu/bob/data.txt"

echo "Question 3:"
Can_she_read? "/cs/home/stu/bob/secret.txt"

echo "Question 4:"
Can_she_remove? "/cs/home/stu/bob/secret.txt"

# Create a new file with permissions and check
echo "Question 5:"
Bobs_new_file "/cs/home/stu/bob/mysecret2.txt"
echo
echo "--------------------------------"
echo "3.4.2 Solutions: "
echo "--------------------------------"

# Define file paths
DATA="/cs/home/stu/bob/data.txt"
bobs_home="/cs/home/stu/bob"

# set/verify the SGID bit on Bobs home directory
set_and_verify_sgid() {
  chmod g+s "$bobs_home"
  # Check SGID bit
  if [ "$(ls -ld "$bobs_home" | cut -c6)" == "s" ]; then
    echo "SGID bit is set on $bobs_home."
  else
    echo "Failed to set SGID bit on $bobs_home."
  fi
}

# check if Bob can change file permissions like in question 1
can_bob_change_permissions() {
  # Check if Bob can write to his home directory and change permissions of data.txt
  if [ -w "$bobs_home" ] && [ -w "$DATA" ]; then
    chgrp csmajor "$DATA"
    chmod 640 "$DATA"
    echo "Yes, Bob can change the permissions. The commands used are:"
    echo "chgrp csmajor $DATA"
    echo "chmod 640 $DATA"
  else
    echo "No, Bob cannot change the permissions as he does not have write access to the directory or file."
  fi
}

# determine the commands for file permissions like in question 2
default_perms() {
  umask 002
  echo "Bob should use the command: umask 002 to set default file permissions."
  
  # Create a new file
  touch "$NEW_FILE"
  echo "Created new file $NEW_FILE with default permissions."
  
  # Change ownership to bob:csmajor
  chown bob:csmajor "$NEW_FILE"
  echo "Changed ownership of $NEW_FILE to bob:csmajor."
}

# set_and_verify_sgid
can_bob_change_permissions
default_perms

echo "Final Permissions:"
ls -l "$DATA"

echo "Permissions for Bob's home directory:"
ls -ld "$bobs_home"
echo
echo "--------------------------------"
echo "3.4.3 Solutions: "
echo "--------------------------------"

sudo setfacl -m u:charlie:r-- /home/alice/treasure.txt

# creating Alice's home directory unless it exists
Alice_needs_a_home...() {
    local Alices_home="/home/alice"

    # Create Alice's home directory if it doesn't exist
    if [[ ! -d "$Alices_home" ]]; then
        echo "Alice's home directory does not exist. Creating the directory."
        mkdir -p "$Alices_home"
        # WARNING: assumes Alice has permission to create her home directory
    else
        echo "Alice's home directory already exists."
    fi
}

# locating and removing possible duplicate copies of the file
delete_treasures() {
    local whats_my_name="treasure.txt"
    local Alices_home="/home/alice"

    # remove duplicates
    find "$Alices_home" -type f -name "$whats_my_name" ! -path "$Alices_home/$whats_my_name" -exec rm {} \; 2>/dev/null && \
    echo "Removed copies of $whats_my_name within the home directory."
}

# configure file with permissions and ACL
treasure_needs_permissions() {
    local file="/home/alice/treasure.txt"

    # Does the file even exist? If not, create it
    if [[ ! -f "$file" ]]; then
        echo "File $file not found. Creating the file."
        touch "$file"
    fi
    echo "File $file is ready."

    # Remove immutable attribute if necessary
    if lsattr "$file" 2>/dev/null | grep -q 'i'; then
        chattr -i "$file"
        echo "Removed immutable attribute from $file."
    fi

    chown alice:alice "$file" && echo "Changed file ownership to Alice."

    chmod 600 "$file" && echo "Changed file permissions to read/write for owner (Alice), no permissions for others."

    # Does the treasure_group even exist? if not, create it
    if ! getent group treasure_group &>/dev/null; then
        groupadd treasure_group && echo "Group 'treasure_group' created."
    fi

    chgrp treasure_group "$file" && chmod 660 "$file" && \
    echo "Changed the file group to 'treasure_group' and set group permissions to read/write."

    setfacl -m u:charlie:r-- "$file" && echo "Set ACL for 'charlie' to read only."

    # Show requested permissions and ACL
    echo "Final permissions for $file:"
    ls -l "$file"
    getfacl "$file" 2>/dev/null || echo "ACL not supported on this system or not present."
}

Alice_needs_a_home...
delete_treasures
treasure_needs_permissions

getent group treasure_group

echo "--------------------------------"
echo "This work complies with the JMU honor code. I did not give or receive unauthorized help on this assignment."