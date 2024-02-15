#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 08:42:58 2023

@author: abrahamreines
"""

import os
import math

def factor(x, lowest=2, factors=None):
    """
    Recursive function to find the prime factors of a given integer x.
    Parameters:
    - x: The integer to factor.
    - lowest: The lowest possible integer factor to start from. Default is 2.
    - factors: The list to store the factors. Default is None.
    Returns:
    - A list containing the prime factors of x.
    Modified: 2023-10-24
    """
    # Initialize the factors list
    if factors is None:
        factors = []
        
    # Handle negative integers
    if x < 0:
        x = abs(x)
        factors.append(-1)
        
    # when x is less than 2, return the factors
    if x < 2:
        return factors
    
    # Check if 'lowest' is a factor of x
    if x % lowest == 0:
        factors.append(lowest)
        return factor(x // lowest, lowest, factors)
    else:
        # Find the next possible factor, starting from 'lowest + 1'
        for next_lowest in range(lowest + 1, int(math.sqrt(x)) + 2):
            if x % next_lowest == 0:
                return factor(x, next_lowest, factors)
                
        # Return x as a prime number
        factors.append(x)
        return factors

def complianceReport():
    """
    This function prints a compliance report based on the provided instructions.
    """
    print("\nCompliance Report")
    print("-----------------")
    print("1. The function is named factor().")
    print("2. It accepts an optional parameter 'lowest' for the lowest possible integer factor of x.")
    print("3. The function uses recursion to find the factors.")
    print("4. Factors are searched between 2 and the square root of x.")
    print("5. If the integer is negative, the function handles it by finding the factors of the positive version and replacing 1 with -1.")
    print("6. The function has been tested on compound, non-prime numbers as well as the special cases of 0 and 1.")
    print("7. Python's built-in list structure is used to assemble the factors.\n")

# Test the function and print compliance report
if __name__ == "__main__":
    print(factor(56))  # Output should be [2, 2, 2, 7]
    print(factor(-56))  # Output should be [-1, 2, 2, 2, 7]
    print(factor(37))  # Output should be [37] since 37 is a prime number
    print(factor(0))  # Output should be []
    print(factor(1))  # Output should be []
    complianceReport()
