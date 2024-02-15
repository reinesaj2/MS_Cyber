#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:04:21 2023

@author: abrahamreines
"""

def identity(x):  
    """Identity function that returns the input value."""
    return x

class OrderedRecordArray(object):
    """
    This class implements an ordered array of records.
    Items are ordered based on a key function.
    """
    
    def __init__(self, initialSize, key=identity):
        """Constructor: Initialize the array with a given size and key function."""
        self.__a = [None] * initialSize  # The underlying array, initialized to None
        self.__nItems = 0  # Number of items in the array, initially 0
        self.__key = key  # Function to obtain the key for ordering
    
    def __len__(self):
        """Return the number of items in the array."""
        return self.__nItems
    
    def get(self, n):
        """Return the value at index n."""
        if n >= 0 and n < self.__nItems:  # Check index bounds
            return self.__a[n]  # Return the item if index is valid
        raise IndexError(f"Index {n} is out of range")
    
    def traverse(self, function=print):
        """Traverse all items in the array and apply a given function."""
        for j in range(self.__nItems):
            function(self.__a[j])
    
    def __str__(self):
        """Convert the array to a string representation."""
        ans = "["  # Initialize string with an opening bracket
        for i in range(self.__nItems):  # Loop through each item
            if len(ans) > 1:
                ans += ", "  # Separate items with a comma
            ans += str(self.__a[i])  # Add the item to the string
        ans += "]"  # Close string with a closing bracket
        return ans
    
    def find(self, key):
        """Find the index at or just below the given key."""
        lo = 0  # Lower boundary of the search
        hi = self.__nItems - 1  # Upper boundary of the search
        while lo <= hi:
            mid = (lo + hi) // 2  # Compute the midpoint for binary search
            if self.__key(self.__a[mid]) == key:  # Key found
                return mid
            elif self.__key(self.__a[mid]) < key:  # Key is in the upper half
                lo = mid + 1
            else:  # Key is in the lower half
                hi = mid - 1
        return lo  # Key not found, return insertion point
    
    def search(self, key):
        """Search for a record by its key and return it if found."""
        idx = self.find(key)
        if idx < self.__nItems and self.__key(self.__a[idx]) == key:
            return self.__a[idx]  # Item found, return it
    
    def insert(self, item):
        """Insert an item into the correct position in the array."""
        if self.__nItems >= len(self.__a):
            raise Exception("Array overflow")  # Array is full
        j = self.find(self.__key(item))  # Find the insertion point
        for k in range(self.__nItems, j, -1):  # Move larger items to the right
            self.__a[k] = self.__a[k - 1]
        self.__a[j] = item  # Insert the new item
        self.__nItems += 1  # Increment the number of items
    
    def delete(self, item):
        """Delete an item from the array."""
        j = self.find(self.__key(item))  # Find the item's index
        if j < self.__nItems and self.__a[j] == item:  # If the item is found
            self.__nItems -= 1  # Decrease the item count
            for k in range(j, self.__nItems):  # Move larger items to the left
                self.__a[k] = self.__a[k + 1]
            return True  # Deletion was successful
        return False  # Item was not found