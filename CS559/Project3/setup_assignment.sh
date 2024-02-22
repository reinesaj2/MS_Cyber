Check to make sure there is nothing interfering: 

#!/bin/bash

# Script to set up users, groups, directories, and file permissions for the assignment

# Define user and group names
users=("alice" "bob" "charlie")
groups=("csmajor" "bobsgroup" "faculty") # Added faculty group

# Create groups if they do not exist
for group in "${groups[@]}"; do
    if ! getent group "$group" &>/dev/null; then
        groupadd "$group"
        echo "Group $group created."
    fi
done

# Create users if they do not exist, add them to groups, and ensure home directories exist
for user in "${users[@]}"; do
    home_dir="/home/${user}"
    if ! id "$user" &>/dev/null; then
        useradd -m -d "$home_dir" "$user"
        echo "User $user created with home directory $home_dir."
    else
        echo "User $user already exists."
        if [ ! -d "$home_dir" ]; then
            echo "Home directory $home_dir not found. Creating it."
            mkdir -p "$home_dir"
            chown "$user:$user" "$home_dir"
        else
            echo "Home directory $home_dir exists."
        fi
    fi
    
# Add user to appropriate groups
    if [ "$user" == "bob" ]; then
        usermod -a -G "${groups[@]}" "$user"
    else
        usermod -a -G "${groups[0]}" "$user"
    fi
done

# Create directory structure for Bob
mkdir -p /cs/home/stu/bob
chown bob:bobsgroup /cs/home/stu/bob
chmod 2750 /cs/home/stu/bob

# Create files and set permissions for Bob
touch /cs/home/stu/bob/{data.txt,secret.txt}

# Correcting the group and permissions of data.txt
chown bob:faculty /cs/home/stu/bob/data.txt
chmod 644 /cs/home/stu/bob/data.txt

# Set execute permission for others on all parent directories
chmod o+x /cs
chmod o+x /cs/home
chmod o+x /cs/home/stu
chmod o+x /cs/home/stu/bob  # This line sets execute permission for others.

# Check and create .bashrc for Bob and set umask
if [ ! -f "$home_dir/.bashrc" ]; then
    echo "Creating .bashrc for Bob."
    touch "$home_dir/.bashrc"
    chown bob:bob "$home_dir/.bashrc"
fi

echo "umask 0133" >> "$home_dir/.bashrc"

# Create treasure.txt file for Alice and set permissions
touch /home/alice/treasure.txt
chown alice:alice /home/alice/treasure.txt
chmod 600 /home/alice/treasure.txt

# Change group of treasure.txt to bobsgroup and set permissions
chgrp bobsgroup /home/alice/treasure.txt
chmod 660 /home/alice/treasure.txt

# Set ACL for Charlie to read the treasure.txt
setfacl -m u:charlie:r /home/alice/treasure.txt

# Ensure that ACLs are enabled on the filesystem
mount -o remount,acl /

# Set the primary group of Alice and Bob to csmajor
usermod -g csmajor alice
usermod -g csmajor bob

# Ensure Alice is in the csmajor group
usermod -a -G csmajor alice

# Ensure data.txt is owned by the group csmajor
# chgrp csmajor /cs/home/stu/bob/data.txt

# Set the setgid bit on the /cs/home/stu/bob directory
chmod g+s /cs/home/stu/bob

# Set permissions for data.txt according to the assignment
chown bob:faculty /cs/home/stu/bob/data.txt
chmod 644 /cs/home/stu/bob/data.txt

# Verify the permissions and ownership of the files and directories
ls -ld /cs/home/stu
ls -ld /cs/home/stu/bob
ls -l /cs/home/stu/bob/data.txt
ls -l /cs/home/stu/bob/secret.txt

echo "Setup complete. Users, groups, permissions, and ACL are set as per requirements."

# Check if Alice can read Bob's data.txt
if sudo -u alice test -r /cs/home/stu/bob/data.txt; then
    echo "Yes, Alice can read Bob's file data.txt."
else
    echo "No, Alice cannot read Bob's file data.txt."
fi

# Check if Alice can remove Bob's data.txt
if sudo -u alice test -w /cs/home/stu/bob/; then
    echo "Yes, Alice can remove Bob's file data.txt."
else
    echo "No, Alice cannot remove Bob's file data.txt."
fi

# Check if Alice can read Bob's secret.txt
if sudo -u alice test -r /cs/home/stu/bob/secret.txt; then
    echo "Yes, Alice can read Bob's file secret.txt."
else
    echo "No, Alice cannot read Bob's file secret.txt."
fi

# Check if Alice can remove Bob's secret.txt
if sudo -u alice test -w /cs/home/stu/bob/; then
    echo "Yes, Alice can remove Bob's file secret.txt."
else
    echo "No, Alice cannot remove Bob's file secret.txt."
fi

# Create a new file as Bob and check the permissions
sudo -u bob bash -c 'echo "My Super Secret is tBd78tsheS" > /cs/home/stu/bob/mysecret2.txt'
echo -n "The full permissions of mysecret2.txt are: "
ls -l /cs/home/stu/bob/mysecret2.txt | cut -d ' ' -f1

# Check if Bob can change permissions to allow all csmajor read access but not others
if sudo -u bob chmod 640 /cs/home/stu/bob/data.txt; then
    echo "Bob has changed the permissions of data.txt to allow csmajor read access."
else
    echo "Bob cannot change the permissions of data.txt."
fi

# Set the default permission for Bob's new files
echo "umask 037" | sudo -u bob tee -a /home/bob/.bashrc
echo "Bob has set the default permissions for his new files."

# For the complex case, set permissions on treasure.txt
sudo -u alice chmod 660 /home/alice/treasure.txt
sudo -u alice setfacl -m u:bob:rw /home/alice/treasure.txt
sudo -u alice setfacl -m u:charlie:r-- /home/alice/treasure.txt

# Check the final permissions and ACLs of treasure.txt
echo -n "The final permissions of treasure.txt are: "
ls -l /home/alice/treasure.txt | cut -d ' ' -f1
echo "The ACL entries for treasure.txt are: "
getfacl /home/alice/treasure.txt | grep -E "^(user|group):"

# Check the ownership and permissions of /cs/home/stu and /cs/home/stu/bob
echo -n "The ownership and permissions of /cs/home/stu are: "
ls -ld /cs/home/stu | cut -d ' ' -f1,3,4
echo -n "The ownership and permissions of /cs/home/stu/bob are: "
ls -ld /cs/home/stu/bob | cut -d ' ' -f1,3,4

# Add checks for the ownership and permissions of data.txt and secret.txt
echo -n "The ownership and permissions of data.txt are: "
ls -l /cs/home/stu/bob/data.txt | cut -d ' ' -f1,3,4
echo -n "The ownership and permissions of secret.txt are: "
ls -l /cs/home/stu/bob/secret.txt | cut -d ' ' -f1,3,4

echo "Setup and verification complete."
