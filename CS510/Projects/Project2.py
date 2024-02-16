#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 12:03:10 2023

# tictac.py

# This program uses functions to draw a tic-tac-toe board with alternating X's 
and O's.
# It defines several functions:
# - print_divider: Prints three minus signs separated by plus signs to create a
 visual divider between rows.
# - print_X_or_O: Takes a number as input and prints an 'O' if the number is 
even, and an 'X' if the number is odd.
# - print_row: Takes a row number as input and calls print_X_or_O to print the 
corresponding X's or O's, separated by vertical bars.
# - print_board: Takes a starting value as input (either 0 or 1) to determine 
whether the first row starts with an 'X' or an 'O'.
#   It calls print_row and print_divider to print the tic-tac-toe board.

# The program concludes by calling print_board with an even argument (0), 
starting the board with an 'X'.

Author: Abraham Reines
"""

# Function to print three minus signs separated by plus signs
def print_divider():
    print("---+---+---")

# Function to print 'X' or 'O' based on the input number
def print_X_or_O(num):
    c = (num % 2) * 9
    print(chr(79 + c), end='')

# Function to print a row with 'X's or 'O's and vertical bars
def print_row(row_num):
    print_X_or_O(row_num)
    print(" | ", end='')
    print_X_or_O(row_num + 1)
    print(" | ", end='')
    print_X_or_O(row_num + 2)
    print()  # Move to the next line

# Function to print the tic-tac-toe board using print_row and print_divider
def print_board(start_with_X):
    print_row(start_with_X)
    print_divider()
    print_row(start_with_X + 3)
    print_divider()
    print_row(start_with_X + 6)

# Calling print_board with an even argument to start with 'X'
print_board(0)