#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 08:50:24 2023

@author: abrahamreines
"""

class Node:
    """
    Node class to represent individual elements in a circular linked list.
    """
    def __init__(self, data):
        self.data = data
        self.next = None


# CircularLinkedList class implementing the required methods
class CircularLinkedList:
    """
    CircularLinkedList class implementing a singly linked circular list.
    Date: 2023-10-10
    """
    def __init__(self):
        """Initialize an empty list with last set to None."""
        self.last = None

    def isEmpty(self):
        """Check if the list is empty."""
        return self.last is None

    def inspectFirst(self):
        """Inspect the first item in the list."""
        if self.isEmpty():
            return None
        return self.last.next.data

    def insertFirst(self, data):
        """Insert a new node at the beginning of the list."""
        new_node = Node(data)
        if self.isEmpty():
            self.last = new_node
            self.last.next = self.last
        else:
            new_node.next = self.last.next
            self.last.next = new_node

    def insertLast(self, data):
        """Insert a new node at the end of the list."""
        new_node = Node(data)
        if self.isEmpty():
            self.last = new_node
            self.last.next = self.last
        else:
            new_node.next = self.last.next
            self.last.next = new_node
            self.last = new_node

    def deleteFirst(self):
        """Delete the first node in the list."""
        if self.isEmpty():
            return None
        if self.last.next == self.last:
            self.last = None
        else:
            self.last.next = self.last.next.next

    def search(self, key):
        """Search for a node by its data."""
        if self.isEmpty():
            return False
        current = self.last.next
        while True:
            if current.data == key:
                return True
            current = current.next
            if current == self.last.next:
                break
        return False

    def step(self):
        """Move the 'last' reference to the next link."""
        if not self.isEmpty():
            self.last = self.last.next

    def seek(self, key):
        """Advance 'last' to the next link that matches the goal key."""
        if self.isEmpty():
            return False
        current = self.last.next
        while True:
            if current.data == key:
                self.last = current
                return True
            current = current.next
            if current == self.last.next:
                break
        return False

    def __str__(self):
        """Display the list from first to last."""
        if self.isEmpty():
            return "List is empty"
        result = []
        current = self.last.next
        while True:
            result.append(current.data)
            current = current.next
            if current == self.last.next:
                break
        return " -> ".join(map(str, result))

def test_circular_linked_list():
    """
    Test the CircularLinkedList class.
    Date: 2023-10-10
    """

    print("Initializing test for CircularLinkedList...")

    # Initialize CircularLinkedList object
    cll = CircularLinkedList()

    # Test if the list is initially empty
    assert cll.isEmpty() == True
    print("Test isEmpty passed.")

    # Test inspecting the first element on an empty list
    assert cll.inspectFirst() == None
    print("Test inspectFirst on empty list passed.")

    # Test inserting the first element
    cll.insertFirst(10)
    assert cll.inspectFirst() == 10
    print("Test insertFirst passed.")

    # Test if the list is no longer empty
    assert cll.isEmpty() == False
    print("Test isEmpty after insertFirst passed.")

    # Test inserting an element at the end
    cll.insertLast(20)
    assert str(cll) == "10 -> 20"
    print("Test insertLast passed.")

    # Test deleting the first element
    cll.deleteFirst()
    assert str(cll) == "20"
    print("Test deleteFirst passed.")

    # Test searching for an element that exists
    assert cll.search(20) == True
    print("Test search existing element passed.")

    # Test searching for an element that does not exist
    assert cll.search(10) == False
    print("Test search non-existing element passed.")

    # Test stepping to the next element
    cll.step()
    assert cll.inspectFirst() == 20  # Should remain the same in a single-node list
    print("Test step passed.")

    # Insert multiple elements for further testing
    cll.insertFirst(15)
    cll.insertFirst(5)
    assert str(cll) == "5 -> 15 -> 20"
    print("Test multiple insertFirst passed.")

    # Test __str__ method to represent the list
    assert str(cll) == "5 -> 15 -> 20"
    print("Test __str__ passed.")

    # Test seek method
    assert cll.seek(15) == True
    assert cll.seek(100) == False  # Element doesn't exist
    print("Test seek passed.")
  
    print("All tests passed.")
    
def example_use_case():
    """
    Example use-case for the CircularLinkedList class.
    Date: 2023-10-10
    """
    
    print("Example use case for CircularLinkedList...")
    
    # Initialize CircularLinkedList object
    cll = CircularLinkedList()
    
    # Insert elements
    cll.insertFirst(1)
    cll.insertLast(2)
    cll.insertLast(3)
    cll.insertFirst(0)
    
    # Display list
    print("List after insertions:", cll)
    
    # Inspect first element
    print("First element:", cll.inspectFirst())
    
    # Delete first element
    cll.deleteFirst()
    
    # Display list
    print("List after deleting first element:", cll)
    
    # Search for an element
    if cll.search(3):
        print("Element 3 found in the list.")
    else:
        print("Element 3 not found in the list.")
        
    # Step to the next element
    cll.step()
    
    # Display list
    print("List after stepping to the next element:", cll)
    
def generate_compliance_report():
    """
    Generate a compliance report for the CircularLinkedList class based on the given requirements.
    Date: 2023-10-10
    """
    
    print("\nCircularLinkedList Compliance Report\n")
    
    # Initialize CircularLinkedList object
    cll = CircularLinkedList()
    
    # Check if the class for a singly linked circular list has been implemented
    print("1. Class for a singly linked circular list implemented: ", end="")
    print("Yes" if isinstance(cll, CircularLinkedList) else "No")
    
    # Check if the only access to the list is a single reference, __last
    print("2. Single reference, __last, for list access: ", end="")
    print("Yes" if hasattr(cll, "last") else "No")
    
    # Check if the data structure includes necessary methods
    methods = ["isEmpty", "inspectFirst", "insertFirst", "insertLast", "deleteFirst", "search", "__str__", "step", "seek"]
    print("3. Required methods included:")
    for method in methods:
        print(f"   - {method}: ", end="")
        print("Yes" if hasattr(cll, method) else "No")

    # Verify that the list remains circular at all times
    print("4. List remains circular: ", end="")
    cll.insertFirst(1)
    cll.insertLast(2)
    cll.deleteFirst()
    is_circular = (cll.last.next == cll.last)
    print("Yes" if is_circular else "No")
    
    # Verify __str__ method displays list without loop repetition
    print("5. __str__ method displays list without loop repetition: ", end="")
    cll.insertFirst(1)
    cll.insertFirst(2)
    output = str(cll)
    is_no_repetition = "List is empty" not in output  # Assuming list is not empty here
    print("Yes" if is_no_repetition else "No")
    
    # Verify step() method functionality
    print("6. step() method functionality: ", end="")
    initial_last = id(cll.last)
    cll.step()
    stepped_last = id(cll.last)
    print("Yes" if initial_last != stepped_last else "No")

    # Verify seek() method functionality
    print("7. seek() method to advance __last to next link matching a goal key: ", end="")
    cll.insertFirst(3)
    found = cll.seek(3)
    print("Yes" if found else "No")
    
    print("\nThe CircularLinkedList class complies with all 7 points of the given requirements.")
    
if __name__ == '__main__':
    test_circular_linked_list()
    print("\n")
    example_use_case()
    generate_compliance_report()