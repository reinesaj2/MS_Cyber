#!/bin/bash

# File name: assignment_solutions_v2.sh
# Author: Abraham Reines
# Date: February 21, 2024
# Modified: February 22, 2024

# Function to check read permission for Alice
can_read() {
  # Check if the file exists and is readable by using test command
  if [ -r "$1" ]; then
    # If file is readable, check if the user 'alice' is either the owner or part of the group with read permission
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

# Function to check remove permission for Alice
can_remove() {
  if sudo -u alice test -w "$1"; then
    echo "yes - Alice can remove the file $1 because she has write permissions."
  else
    echo "no - Alice cannot remove the file $1 because she lacks write permissions."
  fi
}

# Function to simulate the creation of a new file by Bob with specific permissions
create_new_file() {
  sudo -u bob touch "$1"
  sudo -u bob chmod g+s "$1"
  echo "The full permissions for the new file $1 are:"
  ls -l "$1"
}
echo
echo "3.4.1 Solutions:"
echo "--------------------------------"
# Check permissions for Alice
echo "Question 1:"
can_read "/cs/home/stu/bob/data.txt"

echo "Question 2:"
can_remove "/cs/home/stu/bob/data.txt"

echo "Question 3:"
can_read "/cs/home/stu/bob/secret.txt"

echo "Question 4:"
can_remove "/cs/home/stu/bob/secret.txt"

# Create a new file with specific permissions and check
echo "Question 5:"
create_new_file "/cs/home/stu/bob/mysecret2.txt"
echo
echo "--------------------------------"
echo "3.4.2 Solutions: "
echo "--------------------------------"

# Define the file paths
data_txt="/cs/home/stu/bob/data.txt"
bob_home="/cs/home/stu/bob"

# Function to set and verify the SGID bit on Bob's home directory
set_and_verify_sgid() {
  # Set the SGID bit on Bob's home directory
  chmod g+s "$bob_home"
  # Check if SGID bit is set
  if [ "$(ls -ld "$bob_home" | cut -c6)" == "s" ]; then
    echo "SGID bit is set on $bob_home."
  else
    echo "Failed to set SGID bit on $bob_home."
  fi
}

# Function to check if Bob can change the file permissions as specified in question 1
can_bob_change_permissions() {
  # Check if Bob can write to his home directory and change permissions of data.txt
  if [ -w "$bob_home" ] && [ -w "$data_txt" ]; then
    # Set the group of data.txt to 'csmajor'
    chgrp csmajor "$data_txt"
    # Change the permissions of data.txt to be read-only for the group 'csmajor' and no permissions for others
    chmod 640 "$data_txt"
    echo "Yes, Bob can change the permissions. The commands used are:"
    echo "chgrp csmajor $data_txt"
    echo "chmod 640 $data_txt"
  else
    echo "No, Bob cannot change the permissions as he does not have write access to the directory or file."
  fi
}

# Function to determine the commands for setting default file permissions as specified in question 2
set_default_permissions() {
  # Bob wants his files to be readable and writable by himself and the group,
  # and readable but not writable/non-executable by others.
  # The umask value that corresponds to these requirements is 002.
  # This will result in default permissions of 775 for directories and 664 for files.
  umask 002
  echo "Bob should use the command: umask 002"
}

# Execute the functions and print the results
# set_and_verify_sgid
can_bob_change_permissions
set_default_permissions

# Print the final permissions to verify the changes
echo "Final Permissions:"
ls -l "$data_txt"
# Print the permissions of Bob's home directory to verify the SGID bit setting
echo "Permissions for Bob's home directory:"
ls -ld "$bob_home"
echo
echo "--------------------------------"
echo "3.4.3 Solutions: "
echo "--------------------------------"

sudo setfacl -m u:charlie:r-- /home/alice/treasure.txt

# Unique function name for creating Alice's home directory if it doesn't exist
create_alice_home_directory() {
    local home_directory="/home/alice"

    # Create Alice's home directory if it doesn't exist
    if [[ ! -d "$home_directory" ]]; then
        echo "Alice's home directory does not exist. Creating the directory."
        mkdir -p "$home_directory"
        # The script assumes that Alice has permission to create her home directory
    else
        echo "Alice's home directory already exists."
    fi
}

# Unique function name for locating and removing unauthorized copies of the file
remove_unauthorized_copies() {
    local file_name="treasure.txt"
    local home_directory="/home/alice"

    # Find instances of the file within Alice's home directory and remove duplicates
    find "$home_directory" -type f -name "$file_name" ! -path "$home_directory/$file_name" -exec rm {} \; 2>/dev/null && \
    echo "Removed unauthorized copies of $file_name within the home directory."
}

# Function to configure file with proper permissions and ACL
configure_treasure_permissions() {
    local file="/home/alice/treasure.txt"

    # Ensure the file exists
    if [[ ! -f "$file" ]]; then
        echo "File $file not found. Creating the file."
        touch "$file"
    fi
    echo "File $file is ready."

    # Check for immutable attribute and remove it if present
    if lsattr "$file" 2>/dev/null | grep -q 'i'; then
        chattr -i "$file"
        echo "Removed immutable attribute from $file."
    fi

    # Change ownership of the file to Alice
    chown alice:alice "$file" && echo "Changed file ownership to Alice."

    # Change file permissions to read/write for owner (Alice) and no permissions for others
    chmod 600 "$file" && echo "Changed file permissions to read/write for owner (Alice), no permissions for others."

    # Check if the group 'treasure_group' exists; if not, create it
    if ! getent group treasure_group &>/dev/null; then
        groupadd treasure_group && echo "Group 'treasure_group' created."
    fi

    # Change the group ownership of the file to 'treasure_group' and set group permissions
    chgrp treasure_group "$file" && chmod 660 "$file" && \
    echo "Changed the file group to 'treasure_group' and set group permissions to read/write."

    # Set an ACL for Charlie to read only if possible
    setfacl -m u:charlie:r-- "$file" && echo "Set ACL for 'charlie' to read only."

    # Display the final permissions to verify
    echo "Final permissions for $file:"
    ls -l "$file"
    getfacl "$file" 2>/dev/null || echo "ACL not supported on this system or not present."
}

# Call the functions to create home directory, remove unauthorized copies, and configure permissions
create_alice_home_directory
remove_unauthorized_copies
configure_treasure_permissions

getent group treasure_group

echo "--------------------------------"
echo "This work complies with the JMU honor code. I did not give or receive unauthorized help on this assignment."
