#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 08:46:21 2023
Modified on Wed Jun 22 10:00:00 2023
@author: abrahamreines
"""

def pig_latin(word):
    vowels = 'aeiou'
    if word[0] in vowels:
        return word + 'yay'
    elif word[0] == 'y':
        return word[1:] + word[0] + 'ay'
    else:
        consonant_cluster = ''
        for letter in word:
            if letter not in vowels:
                consonant_cluster += letter
            else:
                break
        return word[len(consonant_cluster):] + consonant_cluster + 'ay'

def translate_to_pig_latin(sentence):
    words = sentence.split()
    pig_latin_words = [pig_latin(word.lower()) for word in words]
    return ' '.join(pig_latin_words)

# Ask the user for input
user_input = input("Enter an English sentence: ")
pig_latin_sentence = translate_to_pig_latin(user_input)
print("Pig Latin translation:", pig_latin_sentence)