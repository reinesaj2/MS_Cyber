#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script is a Python program that provides information about U.S. interstate
 highways based on their numbers. 

The program takes a highway number as input from the user and prints out:
- Whether the highway is a primary or auxiliary highway
- If it's an auxiliary highway, the primary highway it serves
- The direction (north/south or east/west) the highway runs

The program uses several functions to perform these tasks:
- Validity(Highway): Checks if the given highway number is valid
- Primary(Highway): Checks if the given highway number is for a primary highway
- GetPrimary(Highway): Returns the primary highway that an auxiliary highway 
serves
- Directions(Highway): Determines the direction of a highway
- Execute(): Main function that interacts with the user, takes the highway 
number as input, and prints the relevant information about the highway

This script was created by Abraham Reines on June 8, 2023.

"""

def Validity(Highway):
    """Check if the highway number is valid."""
    if Highway <= 0 or (Highway >= 100 and Highway % 100 == 0):
        return False
    return True

def Primary(Highway):
    """Check if the highway is primary."""
    return Highway < 100

def GetPrimary(Highway):
    """Get the primary highway for an auxiliary highway."""
    return Highway % 100

def Directions(Highway):
    """Get the direction of the highway."""
    return 'north/south' if Highway % 2 != 0 else 'east/west'

def Execute():
    Highway = int(input('Please enter a highway number: '))

    if not Validity(Highway):
        print(f'{Highway} is not a valid interstate highway number.')
        return

    if Primary(Highway):
        print(f'I-{Highway} is primary, going {Directions(Highway)}.')
    else:
        primary_highway = GetPrimary(Highway)
        print(f'I-{Highway} is auxiliary, serving I-{primary_highway}, going {Directions(primary_highway)}.')

Execute()