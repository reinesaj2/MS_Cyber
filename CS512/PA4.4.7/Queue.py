#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:05:57 2023

@author: abrahamreines
"""
from typing import Optional, Any

class Queue:
    """
    This class implements a Queue data structure using a Python list.
    """
    def __init__(self, size: int):
        """
        Constructor: Initializes the queue with a given maximum size.
        """
        self.__max_size = size
        self.__queue = [None] * size
        self.__front = 1
        self.__rear = 0
        self.__n_items = 0

    def insert(self, item: Any) -> bool:
        """
        Inserts an item at the rear of the queue.
        """
        if self.is_full():
            raise Exception("Queue Overflow")
        self.__rear += 1
        if self.__rear == self.__max_size:
            self.__rear = 0
        self.__queue[self.__rear] = item
        self.__n_items += 1
        return True

    def remove(self) -> Optional[Any]:
        """
        Removes the front item of the queue and returns it.
        """
        if self.is_empty():
            raise Exception("Queue Underflow")
        front = self.__queue[self.__front]
        self.__queue[self.__front] = None
        self.__front += 1
        if self.__front == self.__max_size:
            self.__front = 0
        self.__n_items -= 1
        return front

    def peek(self) -> Optional[Any]:
        """
        Returns the frontmost item without removing it from the queue.
        """
        return None if self.is_empty() else self.__queue[self.__front]

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        """
        return self.__n_items == 0

    def is_full(self) -> bool:
        """
        Checks if the queue is full.
        """
        return self.__n_items == self.__max_size

    def __len__(self) -> int:
        """
        Returns the number of items in the queue.
        """
        return self.__n_items

    def __str__(self) -> str:
        """
        Returns a string representation of the queue.
        """
        ans = "["
        for i in range(self.__n_items):
            if len(ans) > 1:
                ans += ", "
            j = i + self.__front
            if j >= self.__max_size:
                j -= self.__max_size
            ans += str(self.__queue[j])
        ans += "]"
        return ans
    
    def toString(self) -> str:
        """
        Returns a string representation of the queue.
        This is an alias for the __str__ method.
        """
        return self.__str__()
