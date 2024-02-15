"""
-------------------------------------------------------------------------------------------
Author: Abraham Reines
Date: 2023-08-26 
Description: This Python script is designed to implement an Ordered Array of Records data structure.
The data structure uses a class named OrderedRecordArray to manage a dynamically sized array.
Each element in the array can have a key-value pair, and the array is always kept in sorted order
based on the keys. The class provides several methods for operations such as insertion, deletion,
search, and traversal. A special method named 'merge' is also implemented to combine two OrderedRecordArray
objects into a single, sorted array. This merging only happens if the key functions of both arrays are identical.
The code includes a testing function to validate the implementation.
-------------------------------------------------------------------------------------------
"""

import random

# Define the identity function
def identity(x):
    return x

# Define the OrderedRecordArray class
class OrderedRecordArray:
    # Constructor
    def __init__(self, initialSize, key=identity):
        self.__a = [None] * initialSize  # The array stored as a list
        self.__nItems = 0  # No items in array initially
        self.__key = key  # Key function gets record key

    # Method to get length of the array
    def __len__(self):
        return self.__nItems  # Return number of items

    # Method to get an item at a specific index
    def get(self, n):
        if n >= 0 and n < self.__nItems:
            return self.__a[n]
        raise IndexError(f"Index {n} is out of range")

    # Method to traverse all items and apply a function
    def traverse(self, function=print):
        for j in range(self.__nItems):
            function(self.__a[j])

    # Method to convert the array to a string
    def __str__(self):
        ans = "["
        for i in range(self.__nItems):
            if len(ans) > 1:
                ans += ", "
            ans += str(self.__a[i])
        ans += "]"
        return ans

    # Method to find an item's index or insertion point
    def find(self, key):
        lo, hi = 0, self.__nItems - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.__key(self.__a[mid]) == key:
                return mid
            elif self.__key(self.__a[mid]) < key:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    # Method to search for an item by its key
    def search(self, key):
        idx = self.find(key)
        if idx < self.__nItems and self.__key(self.__a[idx]) == key:
            return self.__a[idx]

    # Method to insert an item at the correct position
    def insert(self, item):
        if self.__nItems >= len(self.__a):
            raise Exception("Array overflow")
        j = self.find(self.__key(item))
        for k in range(self.__nItems, j, -1):
            self.__a[k] = self.__a[k - 1]
        self.__a[j] = item
        self.__nItems += 1

    # Method to delete an item
    def delete(self, item):
        j = self.find(self.__key(item))
        if j < self.__nItems and self.__a[j] == item:
            self.__nItems -= 1
            for k in range(j, self.__nItems):
                self.__a[k] = self.__a[k + 1]
            return True
        return False
    
    """
    This method merges another OrderedRecordArray object into the current array.
    The merging only occurs if the key functions of both arrays are identical.
    It returns a message indicating the success or failure of the operation.
    """
    # Method to merge another OrderedRecordArray into this one
    def merge(self, other):
        # Check if both key functions are identical
        if self.__key != other.__key:
            return "Key functions must be identical to merge"
        # Create a new list to hold both arrays
        newSize = self.__nItems + other.__nItems
        new_array = [None] * newSize
        i, j, k = 0, 0, 0
        # Merge the two arrays into the new list
        while i < self.__nItems and j < other.__nItems:
            if self.__key(self.__a[i]) < other.__key(other.__a[j]):
                new_array[k] = self.__a[i]
                i += 1
            else:
                new_array[k] = other.__a[j]
                j += 1
            k += 1
        # Copy remaining elements from self.__a, if any
        while i < self.__nItems:
            new_array[k] = self.__a[i]
            i += 1
            k += 1
        # Copy remaining elements from other.__a, if any
        while j < other.__nItems:
            new_array[k] = other.__a[j]
            j += 1
            k += 1
        # Update the current object
        self.__a = new_array
        self.__nItems = newSize

"""
The test_ordered_record_array function serves as a test suite for the OrderedRecordArray class and its methods.
It creates two arrays, fills them with random numbers, merges one into the other, and prints the results.
"""
# Test the OrderedRecordArray class and the new merge() method
def test_ordered_record_array():
    # Create two OrderedRecordArray objects with initial sizes of 10
    arr1 = OrderedRecordArray(10)
    arr2 = OrderedRecordArray(10)

    # Insert some random numbers into them
    for _ in range(5):
        arr1.insert(random.randint(1, 50))
        arr2.insert(random.randint(1, 50))

    # Display the arrays before merging
    print("Array 1 before merge:", arr1)
    print("Array 2 before merge:", arr2)

    # Merge arr2 into arr1
    merge_result = arr1.merge(arr2)

    # Show the result of the merge operation and the contents of the resulting array
    print(f"Merge result: {merge_result}")
    print("Array 1 after merge:", arr1)

    # Create another OrderedRecordArray object with a different key function
    arr3 = OrderedRecordArray(10, key=lambda x: -x)

    # Try to merge arr3 into arr1 (should fail because key functions are different)
    merge_result_diff_key = arr1.merge(arr3)
    print(f"Merge result with different key functions: {merge_result_diff_key}")

# Run the test function
if __name__ == "__main__":
    test_ordered_record_array()
