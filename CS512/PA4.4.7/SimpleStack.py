#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:04:50 2023

@author: abrahamreines
"""

from typing import Optional, Any

class Stack:
    """
    This class implements a Stack data structure using a Python list.
    """
    def __init__(self, max_size: int):
        """
        Constructor: Initializes the stack with a given maximum size.
        """
        self.__stack_list = [None] * max_size  # The stack stored as a list
        self.__top = -1  # No items initially

    def push(self, item: Any) -> None:
        """
        Pushes an item onto the stack.
        """
        if self.is_full():
            raise Exception("Stack Overflow")
        self.__top += 1
        self.__stack_list[self.__top] = item  # Store item

    def pop(self) -> Optional[Any]:
        """
        Pops the top item off the stack and returns it.
        """
        if self.is_empty():
            raise Exception("Stack Underflow")
        top = self.__stack_list[self.__top]
        self.__stack_list[self.__top] = None  # Remove item reference
        self.__top -= 1  # Decrease the pointer
        return top  # Return top item

    def peek(self) -> Optional[Any]:
        """
        Returns the top item without removing it from the stack.
        """
        if not self.is_empty():
            return self.__stack_list[self.__top]  # Return the top item
            
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        """
        return self.__top == -1

    def is_full(self) -> bool:
        """
        Checks if the stack is full.
        """
        return self.__top >= len(self.__stack_list) - 1

    def __len__(self) -> int:
        """
        Returns the number of items on the stack.
        """
        return self.__top + 1

    def __str__(self) -> str:
        """
        Returns a string representation of the stack.
        """
        return "[" + ", ".join(str(self.__stack_list[i]) for i in range(self.__top + 1)) + "]"