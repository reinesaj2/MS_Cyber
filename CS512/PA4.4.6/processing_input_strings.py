#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:01:19 2023

@author: abrahamreines
"""

import os

# Determine the directory of the current script
script_dir = os.path.dirname(__file__)
# Compute the directory path
dir = os.path.join(script_dir, '')

class Queue(object):
    """
    This class implements a Queue data structure using a circular array.
    The array is represented by __que, and its maximum size is set by __maxSize.
    """
    
    def __init__(self, size):
        """Constructor: Initializes the Queue with a given size."""
        self.__maxSize = size  # Maximum size of the circular array
        self.__que = [None] * size  # Initialize the array with None values
        self.__front = 1  # Front of the queue, initially set to 1
        self.__rear = 0  # Rear of the queue, initially set to 0
        self.__nItems = 0  # Number of items in the queue, initially 0

    def insert(self, item):
        """Insert an item at the rear of the queue."""
        if self.isFull():
            raise Exception("Queue overflow")  # Queue is full, raise an exception
        self.__rear += 1  # Move rear one position to the right
        # Check for wrap-around
        if self.__rear == self.__maxSize:
            self.__rear = 0  # Reset rear to the beginning of the array
        self.__que[self.__rear] = item  # Insert the item at the rear position
        self.__nItems += 1  # Increment the number of items in the queue

    def remove(self):
        """Remove and return the item at the front of the queue."""
        if self.isEmpty():
            raise Exception("Queue underflow")  # Queue is empty, raise an exception
        front = self.__que[self.__front]  # Retrieve the front item
        self.__que[self.__front] = None  # Remove the front item by setting it to None
        self.__front += 1  # Move front one position to the right
        # Check for wrap-around
        if self.__front == self.__maxSize:
            self.__front = 0  # Reset front to the beginning of the array
        self.__nItems -= 1  # Decrement the number of items in the queue
        return front  # Return the removed item

    def isEmpty(self):
        """Check if the queue is empty."""
        return self.__nItems == 0

    def isFull(self):
        """Check if the queue is full."""
        return self.__nItems == self.__maxSize

    def __len__(self):
        """Return the number of items in the queue."""
        return self.__nItems

    def __str__(self):
        """Convert the queue to a string representation."""
        ans = "["  # Initialize the string with an opening bracket
        for i in range(self.__nItems):  # Iterate through the items in the queue
            if len(ans) > 1:
                ans += ", "  # Add a comma for separation
            j = i + self.__front  # Calculate the index offset from the front
            # Check for wrap-around
            if j >= self.__maxSize:
                j -= self.__maxSize  # Reset the index to the beginning of the array
            ans += str(self.__que[j])  # Append the item to the string
        ans += "]"  # Close the string with a closing bracket
        return ans

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
        return False  # Item was not found.

# Initialize OrderedRecordArray to hold queues
queue_record = OrderedRecordArray(initialSize=4)

# Function to initialize queues and records
def initialize_queues():
    global queue_record
    queue_record = OrderedRecordArray(initialSize=4)
    
    queueA = Queue(10)
    queueB = Queue(10)
    queueC = Queue(10)
    queueD = Queue(10)
    
    queue_record.insert(('A', queueA))
    queue_record.insert(('B', queueB))
    queue_record.insert(('C', queueC))
    queue_record.insert(('D', queueD))
    return {'A': 0, 'B': 0, 'C': 0, 'D': 0}
                
# Function to process input strings
def process_string(input_str, customer_count, timeline):
    """Process an input string to simulate the checkout lines"""
    global queue_record  # Keeping the global reference to queue_record

    for ch in input_str:
        if ch.isalpha():
            # Manual iteration to find the correct queue
            for i in range(len(queue_record)):
                label, queue = queue_record.get(i)
                if label == ch.upper():
                    break

            if ch.islower():
                # Add a customer to the queue
                customer_count[ch.upper()] += 1
                try:
                    queue.insert(f"{ch.upper()}{customer_count[ch.upper()]}")
                except Exception as e:
                    print(f"Error in Queue {ch.upper()}: {e}")

            else:
                # Process a customer from the queue
                try:
                    queue.remove()
                except Exception as e:
                    print(f"Error in Queue {ch}: {e}")

        else:
            # Record the current content of each queue
            snapshot = {}
            for i in range(len(queue_record)):
                label, queue = queue_record.get(i)
                snapshot[label] = str(queue)
            timeline.append(snapshot)

# Function to print a report for the assignment
def print_report(test_strings):
    """
    Print a detailed report based on the simulation of checkout lines for the given test strings.
    """
    # Header information
    print("Checkout Line Simulation Report")
    print("=" * 40)
    
    # Iterate over each test string and process it
    for index, s in enumerate(test_strings):
        customer_count = initialize_queues()  # Initialize queues and customer_count for each test case
        timeline = []  # Initialize the timeline for this test case
        print(f"Test Case {index + 1}: Processing string: {s}")
        process_string(s, customer_count, timeline)
        
        # Print the timeline
        for time, snapshot in enumerate(timeline):
            print(f"Time {time + 1}:")
            for label, queue in snapshot.items():
                print(f"Queue {label}: {queue}")
        print("-" * 40)
    
    print("End of Report")
    print("=" * 40)

# Sample usage with the provided test strings
test_strings = [
    "aaaa,AAbcd,",
    "abababcabc,Adb,Adb,Ca,",
    "dcbadcbaDCBA-dddAcccBbbbCaaaD-"
]

# Call the function to print the report
print_report(test_strings)