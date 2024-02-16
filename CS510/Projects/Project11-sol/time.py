#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the definition of the class 'Time', which is used to represent the length of a song in minutes and seconds.
The class is designed to be used in a playlist management system, where it will allow for the storage, display, and comparison of song lengths.

Created on Mon Jul 31 16:22:06 2023

Author: Abraham Reines
"""

class Time:
    """
    The 'Time' class is used to represent a time length, specifically the length of a song.
    It includes methods to initialize the time, represent it as a string, and compare it to other 'Time' instances.
    """
    def __init__(self, time_str):
        """
        The constructor for the 'Time' class. Takes a string representing time in the format 'minutes:seconds',
        and splits it into separate 'minutes' and 'seconds' integer attributes.
        """
        self.minutes, self.seconds = map(int, time_str.split(':'))

    def __str__(self):
        """
        Return a string representation of the Time instance.

        Returns:
            str: A string representation of the time in the format MM:SS.
        """
        return f"{self.minutes}:{self.seconds:02d}"

    def __lt__(self, other):
        """
        Compare this Time instance with another based on duration.

        Args:
            other (Time): The other Time instance to compare with.

        Returns:
            bool: True if this Time's duration is less than the other's, False otherwise.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds < other.minutes * 60 + other.seconds
        else:
            return NotImplemented

    def __le__(self, other):
        """
        The less-than-or-equal-to comparison method for the 'Time' class. 
        Compares this 'Time' instance to another based on their total length in seconds.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds <= other.minutes * 60 + other.seconds
        else:
            return NotImplemented

    def __eq__(self, other):
        """
        The equality comparison method for the 'Time' class. 
        Compares this 'Time' instance to another based on their total length in seconds.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds == other.minutes * 60 + other.seconds
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        The inequality comparison method for the 'Time' class. C
        ompares this 'Time' instance to another based on their total length in seconds.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds != other.minutes * 60 + other.seconds
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        The greater-than comparison method for the 'Time' class. 
        Compares this 'Time' instance to another based on their total length in seconds.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds > other.minutes * 60 + other.seconds
        else:
            return NotImplemented

    def __ge__(self, other):
        """
        The greater-than-or-equal-to comparison method for the 'Time' class. 
        Compares this 'Time' instance to another based on their total length in seconds.
        """
        if isinstance(other, Time):
            return self.minutes * 60 + self.seconds >= other.minutes * 60 + other.seconds
        else:
            return NotImplemented
