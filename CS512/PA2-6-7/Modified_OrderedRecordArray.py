'''
-------------------------------------------------------------------------------------------
Author: Abraham Reines
Date: 2023-08-30
Description: This Python script is designed to implement a Modified Ordered Array of Records data structure.
The data structure uses a class named ModifiedOrderedRecordArray to manage a dynamically sized array.
Each element in the array can have a key-value pair, and the array is always kept in sorted order
based on the keys. The class provides several methods for operations such as insertion, deletion,
search, and traversal. The code includes modifications for handling duplicate keys and dynamic resizing.
-------------------------------------------------------------------------------------------
'''
import time
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    matplotlib_available = False

# Define the identity function
def identity(x):
    """Returns the input value as is."""
    return x

# Define the ModifiedOrderedRecordArray class
class ModifiedOrderedRecordArray:
    """This class implements an ordered array of records."""
    
    # Constructor
    def __init__(self, initialSize, key=identity):
        """Initialize the array with a given size and key function."""
        self.__a = [None] * initialSize  # The array stored as a list
        self.__nItems = 0  # No items in array initially
        self.__key = key  # Key function to get record key
        self.__maxSize = initialSize  # Store the maximum size

    # Method to get length of the array
    def __len__(self):
        """Returns the number of items in the array."""
        return self.__nItems

    # Method to get an item at a specific index
    def get(self, n):
        """Returns the item at a specific index."""
        if 0 <= n < self.__nItems:
            return self.__a[n]
        raise IndexError(f"Index {n} is out of range")

    # Method to traverse all items and apply a function
    def traverse(self, function=print):
        """Applies a function to all items in the array."""
        for j in range(self.__nItems):
            function(self.__a[j])

    # Method to convert the array to a string
    def __str__(self):
        """Converts the array to a string."""
        ans = "["
        for i in range(self.__nItems):
            if len(ans) > 1:
                ans += ", "
            ans += str(self.__a[i])
        ans += "]"
        return ans

    # Method to find an item's index or insertion point
    def find(self, key):
        """Finds the index or insertion point of a given key."""
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
        """Searches for an item by its key."""
        idx = self.find(key)
        if idx < self.__nItems and self.__key(self.__a[idx]) == key:
            return self.__a[idx]

    # Method to insert an item at the correct position
    def insert(self, item):
        """Inserts an item while maintaining the order of keys."""
        # Task 2.7: Resize the array if needed
        if self.__nItems >= self.__maxSize:
            # Double the maximum size
            self.__maxSize *= 2
            new_array = [None] * self.__maxSize
            new_array[:self.__nItems] = self.__a
            self.__a = new_array

        j = self.find(self.__key(item))
        for k in range(self.__nItems, j, -1):
            self.__a[k] = self.__a[k - 1]
        self.__a[j] = item
        self.__nItems += 1

    # Method to delete an item
    def delete(self, key):
        """Deletes items with a given key."""
        # Task 2.6: Handle duplicate keys
        j = self.find(key)
        deleted = False
        while j < self.__nItems and self.__key(self.__a[j]) == key:
            self.__nItems -= 1
            for k in range(j, self.__nItems):
                self.__a[k] = self.__a[k + 1]
            deleted = True
        return deleted
    
# Function to test the performance of the ModifiedOrderedRecordArray class
def test_array_growth_strategy(initial_size, growth_factor, multiplier_mode=True, n_inserts=10000):
    """Tests the performance of array resizing strategies.
    
    Parameters:
    initial_size (int): Initial size of the array
    growth_factor (int): The factor by which to grow the array size
    multiplier_mode (bool): True if using multiplication, False if using addition
    n_inserts (int): Number of items to insert
    
    Returns:
    float: Time taken for the test
    """
    array = ModifiedOrderedRecordArray(initial_size)
    
    start_time = time.time()
    
    for i in range(n_inserts):
        if len(array) >= array._ModifiedOrderedRecordArray__maxSize:
            if multiplier_mode:
                array._ModifiedOrderedRecordArray__maxSize *= growth_factor
            else:
                array._ModifiedOrderedRecordArray__maxSize += growth_factor
            
            new_array = [None] * array._ModifiedOrderedRecordArray__maxSize
            new_array[:len(array)] = array._ModifiedOrderedRecordArray__a
            array._ModifiedOrderedRecordArray__a = new_array
        
        array.insert(i)
    
    end_time = time.time()
    
    return end_time - start_time

def run_growth_strategy_tests():
    """
    Description: This Python function is designed to run performance tests on the ModifiedOrderedRecordArray class
    to determine the most efficient array growth strategy. The function tests two strategies: growing the array by a 
    fixed amount (addition mode) and growing the array by a fixed multiplier (multiplier mode). The time taken for 
    each mode is measured and displayed, and the most efficient strategy is identified.
    """
    print("Starting performance tests for array growth strategies...")
    # Initialize parameters
    initial_size = 5
    growth_factor_addition = 5  # for addition mode
    growth_factor_multiplier = 2  # for multiplier mode
    n_inserts = 10000  # number of inserts

    # Test the addition mode
    time_addition = test_array_growth_strategy(initial_size, growth_factor_addition, multiplier_mode=False, n_inserts=n_inserts)

    # Test the multiplier mode
    time_multiplier = test_array_growth_strategy(initial_size, growth_factor_multiplier, multiplier_mode=True, n_inserts=n_inserts)

    # Display the results in a formatted manner
    print(f"Time taken in addition mode: {time_addition:.4f} seconds")
    print(f"Time taken in multiplier mode: {time_multiplier:.4f} seconds")
    
    # Determine the more efficient strategy
    efficient_strategy = "multiplier mode" if time_multiplier < time_addition else "addition mode"
    print(f"From these results, it's evident that the {efficient_strategy} is more efficient for growing the array.")

def plot_growth_strategy_performance():
    """Plots the performance of array growth strategies."""
    # Initialize parameters
    initial_size = 5
    growth_factor_addition = 5  # for addition mode
    growth_factor_multiplier = 2  # for multiplier mode
    n_inserts_list = [1000, 5000, 10000, 15000]  # varying number of inserts
    
    time_addition_list = []
    time_multiplier_list = []
    
    # Run tests and collect time data
    for n_inserts in n_inserts_list:
        time_addition = test_array_growth_strategy(initial_size, growth_factor_addition, multiplier_mode=False, n_inserts=n_inserts)
        time_multiplier = test_array_growth_strategy(initial_size, growth_factor_multiplier, multiplier_mode=True, n_inserts=n_inserts)
        
        time_addition_list.append(time_addition)
        time_multiplier_list.append(time_multiplier)
    
    if matplotlib_available:
        # Create the scientific plot using matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(n_inserts_list, time_addition_list, marker='o', label='Addition Mode')
        plt.plot(n_inserts_list, time_multiplier_list, marker='x', label='Multiplier Mode')
        
        plt.xlabel('Number of Inserts')
        plt.ylabel('Time (seconds)')
        plt.title('Performance of Array Growth Strategies')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        # Create a simple ASCII plot for terminal display
        print("Matplotlib not available. Displaying ASCII plot in terminal:")
        for i in range(len(n_inserts_list)):
            print(f"{n_inserts_list[i]} Inserts: Addition Mode ({time_addition_list[i]:.4f}s) {'*' * int(time_addition_list[i] * 100)}")
            print(f"{n_inserts_list[i]} Inserts: Multiplier Mode ({time_multiplier_list[i]:.4f}s) {'*' * int(time_multiplier_list[i] * 100)}")

if __name__ == '__main__':
    run_growth_strategy_tests()
    plot_growth_strategy_performance()
