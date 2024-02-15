#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:18:37 2023

Author: Abraham Reines
"""

from concurrent.futures import ThreadPoolExecutor
import time
import random
import timeit

class Array(object):

    def __init__(self, initialSize):  # Constructor
        self.__a = [None] * initialSize  # The array stored as a list
        self.__nItems = 0  # No items in array initially

    def __len__(self):
        return self.__nItems  # Return number of items

    def get(self, n):
        if 0 <= n < self.__nItems:  # Check if n is in bounds, and
            return self.__a[n]  # only return item if in bounds

    def set(self, n, value):  # Set the value at index n
        if 0 <= n < self.__nItems:  # Check if n is in bounds, and
            self.__a[n] = value  # only set item if in bounds

    def swap(self, j, k):  # Swap the values at 2 indices
        if 0 <= j < self.__nItems and 0 <= k < self.__nItems:  # Check if indices are in bounds, before processing
            self.__a[j], self.__a[k] = self.__a[k], self.__a[j]

    def insert(self, item):             # Insert item at end
        self.__a[self.__nItems] = item  # Item goes at current end
        self.__nItems += 1              # Increment number of items

    def find(self, item):               # Find index for item
        for j in range(self.__nItems):  # Among current items
            if self.__a[j] == item:     # If found,
                return j                # then return index to element
        return -1                       # Not found -> return -1

    def search(self, item):               # Search for item
        return self.get(self.find(item))  # and return item if found

    def delete(self, item):                 # Delete first occurrence
        for j in range(self.__nItems):      # of an item
            if self.__a[j] == item:
                self.__nItems -= 1
                for k in range(j, self.__nItems):  # Move items from
                    self.__a[k] = self.__a[k + 1]  # right over 1
                return True  # Return success flag
        return False  # Made it here, so couldn’t find the item

    def traverse(self, function=print):  # Traverse all items
        for j in range(self.__nItems):  # and apply a function
            function(self.__a[j])

    def __str__(self):                  # Special def for str() func
        ans = "["                       # Surround with square brackets
        for i in range(self.__nItems):  # Loop through items
            if len(ans) > 1:            # Except next to left bracket,
                ans += ", "             # separate items with comma
            ans += str(self.__a[i])     # Add string form of item
        ans += "]"                      # Close with right bracket
        return ans

    def bubbleSort(self):
        """This method implements the bubble sort algorithm. It iterates through the array multiple times, 
            each time moving the largest unsorted value to its correct position. The process continues until 
            the array is sorted."""
        for last in range(self.__nItems - 1, 0, -1):  # and bubble up
            for inner in range(last):  # inner loop goes up to last
                if self.__a[inner] > self.__a[inner + 1]:  # If elem less
                    self.swap(inner, inner + 1)  # than adjacent value, swap

    def selectionSort(self):  # Sort by selecting min and
        """This method implements the selection sort algorithm. It works by repeatedly finding the minimum 
            element from the unsorted portion and swapping it with the first element of the unsorted portion."""
        for outer in range(self.__nItems - 1):  # swapping min to leftmost
            min = outer  # Assume min is leftmost
            for inner in range(outer + 1, self.__nItems):  # Hunt to right
                if self.__a[inner] < self.__a[min]:  # If we find new min,
                    min = inner  # update the min index
            self.swap(outer, min)  # Swap leftmost and min

    def insertionSort(self):  # Sort by repeated inserts
        """This method implements the insertion sort algorithm. It builds a sorted portion of the array one 
            element at a time by repeatedly picking the next element and inserting it at the correct position 
            within the sorted portion."""
        for outer in range(1, self.__nItems):  # Mark one element
            temp = self.__a[outer]  # Store marked elem in temp
            inner = outer  # Inner loop starts at mark
            while inner > 0 and temp < self.__a[inner - 1]:  # If marked
                self.__a[inner] = self.__a[inner - 1]  # elem smaller, then
                inner -= 1  # shift elem to right
            self.__a[inner] = temp  # Move marked elem to ’hole’
    
    def oddEvenSort(self):
        """This method implements the odd-even sort algorithm optimized with threading.
        It performs two phases in each pass: one for odd indices and one for even indices.
        The method continues until no swaps are required, indicating the array is sorted.
        It returns the number of passes required to sort the array."""
        try:
            # Dynamic thread pool size based on the length of the array
            thread_pool_size = min(4, len(self.__a) // 2)
            thread_pool = ThreadPoolExecutor(max_workers=thread_pool_size)
            is_sorted = False
            passes = 0
    
            while not is_sorted:
                is_sorted = True  # Assume the array is sorted at the beginning of each pass
                passes += 1
    
                # Odd phase
                futures = [thread_pool.submit(parallel_sort, (self.__a, i, True)) for i in range(1, len(self.__a) - 1, 2)]
                if any(future.result() for future in futures):
                    is_sorted = False
                else:
                    # If no swaps occurred during the odd phase, terminate early
                    break
    
                # Even phase
                futures = [thread_pool.submit(parallel_sort, (self.__a, i, False)) for i in range(0, len(self.__a) - 1, 2)]
                if any(future.result() for future in futures):
                    is_sorted = False
    
            return passes
        except Exception as e:
            print(f"Error in oddEvenSort: {e}")
            return None


def parallel_sort(args):
    """This function is a helper function which sorts a pair of elements in the array.
    It takes a tuple containing the array, index, and a boolean indicating the phase (odd or even).
    It returns True if a swap occurred, otherwise False."""
    try:
        array, i, is_odd = args
        if (is_odd and i % 2 == 1 and array[i] > array[i + 1]) or (not is_odd and i % 2 == 0 and array[i] > array[i + 1]):
            array[i], array[i + 1] = array[i + 1], array[i]
            return True
        return False
    except Exception as e:
        print(f"Error in parallel_sort: {e}")
        return False
    
def initArray(size=100, maxValue=100, seed=3.14159):
    """Create an Array of the specified size with a fixed sequence of 'random' elements"""
    arr = Array(size)
    random.seed(seed)
    for i in range(size):
        arr.insert(random.randrange(maxValue))  # Insert random numbers
    return arr  # Return the filled Array

if __name__ == "__main__":

    # Creating an instance of the Array class and inserting values in reverse order
    arr = Array(10)
    for i in range(9, -1, -1):
        arr.insert(i)

    # Displaying the original array and performing odd-even sort
    print("Original array:", arr)
    start_time = time.time()
    passes = arr.oddEvenSort()
    end_time = time.time()
    print(f"Sorted array: {arr}, \n\nNumber of passes: {passes}")
    print(f"Time taken: {end_time - start_time} seconds\n")

    # Testing with a partially sorted array
    arr = Array(10)
    for i in [1, 3, 2, 4, 6, 5, 7, 9, 8, 0]:
        arr.insert(i)

    # Displaying the original array and performing odd-even sort
    print("Original array:", arr)
    start_time = time.time()
    passes = arr.oddEvenSort()
    end_time = time.time()
    print(f"Sorted array: {arr}, \n\nNumber of passes: {passes}")
    print(f"Time taken: {end_time - start_time} seconds\n")

    # Testing with a larger, randomly shuffled array
    arr = Array(1000)
    elements = list(range(1000))
    random.shuffle(elements)
    for i in elements:
        arr.insert(i)

    # Displaying the original array and performing odd-even sort
    print("Original array: Array with 1000 randomly shuffled elements")
    start_time = time.time()
    passes = arr.oddEvenSort()
    end_time = time.time()
    print(f"\nSorted array: Array with 1000 elements")
    print(f"\nNumber of passes: {passes}")
    print(f"\nTime taken: {end_time - start_time} seconds\n")
    
    # Additional testing with initArray function and other sorting methods
    arr = initArray()
    print("Array containing", len(arr), "items:\n", arr)
    for test in ['\ninitArray().bubbleSort()', '\ninitArray().selectionSort()', '\ninitArray().insertionSort()']:
        elapsed = timeit.timeit(test, number=100, globals=globals())
        print(test, "took", elapsed, "seconds", flush=True)
    arr.insertionSort()
    print('\nSorted array contains:\n', arr)
