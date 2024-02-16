#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:40:13 2023

This script is the main program that uses both the hash and db modules to scan 
a given directory and check whether the files in the directory are known (i.e., 
their hashes are in the database). The scan() function takes a directory and a 
database as arguments, computes hashes for all the files in the directory, looks 
up these hashes in the database, and prints out whether each file matches a known 
file (and if so, which one) or is unknown. If the script is executed directly 
from the command line with a directory name as an argument, it will create a 
database for files in the "whitelist" and "blacklist" directories and then scan 
the given directory.

Author: Abraham Reines, Modified: July 20, 2023
"""

# Importing required modules
import os
import sys
import hash  # Imported hash module for hash computation
import db  # Imported db module for database operations

# Function to scan a directory and print matches from a given hash database
def scan(directory, database):
    files = os.listdir(directory)  # List all files in the scan directory

    # Loop over all files in the scan directory
    for file in files:
        filepath = os.path.join(directory, file)  # Get the full path of the file

        # Compute the file hash using the hashfile function from the hash module
        file_hash = hash.hashfile(filepath)

        # Lookup the file hash in the hash database
        match = db.lookup(database, file_hash)

        if match:
            # If a match is found, print the file path and the match
            print(f"{filepath}: matches {os.path.basename(match)}")
        else:
            # If no match is found, print that there is no match
            print(f"{filepath}: No Match")

# Main execution
if __name__ == "__main__":
    directory = sys.argv[1]  # Get the scan directory from the command line arguments
    directories = ["whitelist", "blacklist"]  # Define the directories to be used

    # Create the hash database from the files in the defined directories
    database = db.create_database(directories)

    # Scan the directory using the created hash database
    scan(directory, database)
