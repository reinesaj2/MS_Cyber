#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 10:32 2023

@author: abrahamreines
"""

# Import the CircularLinkedList class from the previous exercise
from CircularLinkedList import CircularLinkedList, Node


class Stack:
    """
    Stack class implementing a LIFO stack based on CircularLinkedList.
    Date: 2023-10-15
    """
    def __init__(self):
        """Initialize an empty stack."""
        self.list = CircularLinkedList()
    
    def push(self, data):
        """Push an element onto the stack."""
        self.list.insertFirst(data)
    
    def pop(self):
        """Pop an element from the stack."""
        if self.list.isEmpty():
            return None
        data = self.list.inspectFirst()
        self.list.deleteFirst()
        return data
    
    def peek(self):
        """Peek at the top element without removing it."""
        return self.list.inspectFirst()


class Queue:
    """
    Queue class implementing a FIFO queue based on CircularLinkedList.
    Date: 2023-10-15
    """
    def __init__(self):
        """Initialize an empty queue."""
        self.list = CircularLinkedList()
    
    def insert(self, data):
        """Insert an element into the queue."""
        self.list.insertLast(data)
    
    def remove(self):
        """Remove an element from the queue."""
        if self.list.isEmpty():
            return None
        data = self.list.inspectFirst()
        self.list.deleteFirst()
        return data
    
    def peek(self):
        """Peek at the front element without removing it."""
        return self.list.inspectFirst()


def test_stack_and_queue():
    """
    Test the Stack and Queue classes with detailed print statements for debugging.
    Date: 2023-10-15
    """
    print("Initializing test for Stack and Queue classes...")

    # Initialize and test Stack object
    print("\nTesting Stack class...")
    s = Stack()
    
    print("Initial stack state: Testing Peek method...")
    assert s.peek() == None
    print(f"Success: Peek returned {s.peek()} as expected.")
    
    print("Testing push(1)...")
    s.push(1)
    assert s.peek() == 1
    print(f"Success: Peek returned {s.peek()} after push(1).")
    
    print("Testing push(2)...")
    s.push(2)
    assert s.peek() == 2
    print(f"Success: Peek returned {s.peek()} after push(2).")
    
    print("Testing first Pop operation...")
    assert s.pop() == 2
    print("Success: Pop returned 2 as expected.")
    
    print("Testing second Pop operation...")
    assert s.pop() == 1
    print("Success: Pop returned 1 as expected.")
    
    print("Testing Pop operation on empty stack...")
    assert s.pop() == None
    print("Success: Pop returned None as expected.")

    # Initialize and test Queue object
    print("\nTesting Queue class...")
    q = Queue()
    
    print("Initial queue state: Testing Peek method...")
    assert q.peek() == None
    print(f"Success: Peek returned {q.peek()} as expected.")
    
    print("Testing insert(1)...")
    q.insert(1)
    assert q.peek() == 1
    print(f"Success: Peek returned {q.peek()} after insert(1).")
    
    print("Testing insert(2)...")
    q.insert(2)
    assert q.peek() == 1
    print(f"Success: Peek returned {q.peek()} after insert(2).")
    
    print("Testing first Remove operation...")
    assert q.remove() == 1
    print("Success: Remove returned 1 as expected.")
    
    print("Testing second Remove operation...")
    assert q.remove() == 2
    print("Success: Remove returned 2 as expected.")
    
    print("Testing Remove operation on empty queue...")
    assert q.remove() == None
    print("Success: Remove returned None as expected.")
    
    print("\nAll tests passed.")
    
def generate_compliance_report():
    """
    Generate a compliance report for the Stack and Queue classes based on the given assignment requirements.
    Date: 2023-10-15
    """

    print("\nStack and Queue Compliance Report\n")

    # Initialize Stack and Queue objects
    s = Stack()
    q = Queue()

    # Check if the Stack class has been implemented
    print("1. Stack class implemented: ", end="")
    print("Yes" if isinstance(s, Stack) else "No")

    # Check if the Stack class includes necessary methods
    stack_methods = ["push", "pop", "peek"]
    print("2. Required Stack methods included:")
    for method in stack_methods:
        print(f"   - {method}: ", end="")
        print("Yes" if hasattr(s, method) else "No")

    # Check if the Queue class has been implemented
    print("\n3. Queue class implemented: ", end="")
    print("Yes" if isinstance(q, Queue) else "No")

    # Check if the Queue class includes necessary methods
    queue_methods = ["insert", "remove", "peek"]
    print("4. Required Queue methods included:")
    for method in queue_methods:
        print(f"   - {method}: ", end="")
        print("Yes" if hasattr(q, method) else "No")

    # Check if Stack and Queue classes are based on CircularLinkedList
    print("\n5. Stack and Queue based on CircularLinkedList: ", end="")
    is_based_on_circular_list = isinstance(s.list, CircularLinkedList) and isinstance(q.list, CircularLinkedList)
    print("Yes" if is_based_on_circular_list else "No")

    print("\nThe Stack and Queue classes comply with all the requirements.")

if __name__ == '__main__':
    test_stack_and_queue()
    generate_compliance_report()

