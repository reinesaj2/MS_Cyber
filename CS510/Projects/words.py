#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:32:20 2023

@author: abrahamreines
"""

def is_dijkstra(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(alphabet) - 2):
        if alphabet[i:i+3] in word:
            return True
    return False

def has_exactly(count, char, word):
    return word.count(char) == count

def has_no_double(word):
    for i in range(len(word) - 1):
        if word[i] == word[i+1]:
            return False
    return True

# Test the functions
print(is_dijkstra('dijkstra'))  # Expected: True
print(has_exactly(3, 'd', 'studded'))  # Expected: True
print(has_no_double('turing'))  # Expected: True
print(has_no_double('hopper'))  # Expected: False
print('\n')

# Open the file
with open('/cs/home/stu/reinesaj/week6/words.txt', 'r') as f:
    words = f.read().splitlines()

# Analyze the words
for word in words:
    # Check if the word has three consecutive letters from the alphabet
    if not is_dijkstra(word):
        continue

    # Check if the word has exactly four of some letter
    if not any(has_exactly(4, char, word) for char in set(word)):
        continue

    # Check if the word has no consecutive double letters
    if not has_no_double(word):
        continue

    print(word)