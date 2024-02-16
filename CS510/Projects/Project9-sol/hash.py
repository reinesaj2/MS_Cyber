#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:39:36 2023

This script is a module that provides a function to calculate the SHA-256 hash 
of a given file. The main function in this script is hashfile(), which takes a 
filename as an argument and returns the SHA-256 hash of the file. If it cannot 
compute the hash (due to, for example, the file not existing), it returns an 
empty string. If the script is executed directly from the command line with a 
filename as an argument, it will print out the filename and the computed hash.

Author: Abraham Reines, Modified: July 20, 2023
"""

# Importing the hashlib module for hash computation
import hashlib

# Function to compute the SHA-256 hash of a file
def hashfile(filename):
    try:
        # Open the file in read-binary mode
        with open(filename, 'rb') as file:
            file_content = file.read()  # Read the content of the file

        # Compute the SHA-256 hash of the file content
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        return file_hash  # Return the computed hash
    except:
        return ""  # Return an empty string in case of any exception

# Main execution
if __name__ == "__main__":
    import sys  # Importing the sys module to access command line arguments

    # Get the filename from the command line arguments
    filename = sys.argv[1]

    # Print the filename and its computed hash
    print(f"{filename} {hashfile(filename)}")
