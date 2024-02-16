#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:39:54 2023

This script is a module that provides functionality to create a database of 
hashes for known files and to look up file paths in this database using hashes. 
The create_database() function creates this database by iterating over files 
in given directories, computing their hashes using the hashfile() function from 
the hash module, and storing the hashes and corresponding file paths in a 
dictionary. The lookup() function takes a hash and a database as arguments, and 
returns the corresponding file path if the hash is found in the database, or an 
empty string otherwise. If the script is executed directly from the command line, 
it will create a database for files in the "whitelist" and "blacklist" 
directories and print out all the hashes and corresponding file paths.

Author: Abraham Reines, Modified: July 20, 2023
"""

# Importing required modules
import os
import hash  # Imported hash module for hash computation

# Function to create a hash database from the files in the given directories
def create_database(directories):
    database = {}  # Initialize an empty hash database

    # Loop over all directories
    for directory in directories:
        files = os.listdir(directory)  # List all files in the directory

        # Loop over all files in the directory
        for file in files:
            filepath = os.path.join(directory, file)  # Get the full path of the file

            # Compute the file hash using the hashfile function from the hash module
            file_hash = hash.hashfile(filepath)
            
            # Add the file hash and file path to the hash database
            database[file_hash] = filepath

    # Return the created hash database
    return database

# Function to lookup a file path in the hash database using a hash
def lookup(database, hash):
    try:
        # Try to return the file path for the given hash
        return database[hash]
    except KeyError:
        # If the hash is not found in the hash database, return an empty string
        return ""

# Main execution
if __name__ == "__main__":
    directories = ["whitelist", "blacklist"]  # Define the directories to be used

    # Create the hash database from the files in the defined directories
    database = create_database(directories)

    # Print all hashes and corresponding file paths in the hash database
    for hash, filename in database.items():
        print(f"{hash} {filename}")
