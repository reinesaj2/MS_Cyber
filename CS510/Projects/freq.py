#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:31:40 2023

@author: abrahamreines

This Python script performs text analysis on a file with one word per line. It 
includes functions to:

1. Read the file and create a dictionary of word frequencies.
2. Calculate and print the total number of words in the file.
3. Calculate and print the number of unique words in the file.
4. Find and print the most frequently occurring word(s) and their frequency.
5. Calculate and print the frequency of each letter in the file, as a percentage 
to two decimal places.
6. Find and print how many times a specific word appears in the file.
7. Find and print all words that appear a certain number of times in the file.

The script is designed to be modular, allowing each function to be used 
independently as needed. To use the script, the file path needs to be provided, 
and specific words or frequencies can be provided as arguments to the relevant 
functions.
"""

# Import necessary libraries
from collections import Counter
import string

# Function to read the file and create a dictionary of word frequencies
def read_file_and_get_word_frequencies(filename):
    word_freq = {}
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip().lower()  # Remove whitespace and convert to lowercase
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    return word_freq

# Function to calculate the total number of words
def total_number_of_words(word_freq):
    return sum(word_freq.values())

# Function to calculate the number of unique words
def number_of_unique_words(word_freq):
    return len(word_freq)

# Function to find the most frequent words
def most_frequent_words(word_freq):
    max_freq = max(word_freq.values())
    most_freq_words = [word for word, freq in word_freq.items() if freq == max_freq]
    return most_freq_words, max_freq

# Function to calculate the frequency of each letter as a percentage
def letter_frequencies(word_freq):
    letter_freq = Counter()
    for word, freq in word_freq.items():
        for letter in word:
            if letter in string.ascii_lowercase:
                letter_freq[letter] += freq
    total_letters = sum(letter_freq.values())
    letter_freq_percent = {letter: round((freq / total_letters) * 100, 2) for letter, freq in letter_freq.items()}
    return letter_freq_percent

# Function to count how many times a specific word appears
def word_appearance(word_freq):
    word = input("Enter a word: ")
    freq = word_freq.get(word, 0)
    print(f"The word '{word}' appears {freq} times")

# Function to find all words that appear a certain number of times
def words_with_frequency(word_freq):
    freq = int(input("Enter a frequency: "))
    words_with_given_freq = [word for word, word_freq in word_freq.items() if word_freq == freq]
    print(f"Words that appear {freq} times: {words_with_given_freq}")

# Main script
if __name__ == "__main__":
    filename = input("Enter the path to your file: ")
    word_freq = read_file_and_get_word_frequencies(filename)

    print(f"Total number of words: {total_number_of_words(word_freq)}")
    print(f"Number of unique words: {number_of_unique_words(word_freq)}")

    most_freq_words, max_freq = most_frequent_words(word_freq)
    print(f"Most frequent word(s): {most_freq_words} appearing {max_freq} times")

    print(f"Letter frequencies: {letter_frequencies(word_freq)}")

    word_appearance(word_freq)
    words_with_frequency(word_freq)