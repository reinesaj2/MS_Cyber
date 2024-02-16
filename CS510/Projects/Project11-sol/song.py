# song.py - a class that represents a song
# Author: Abraham Reines
# Created: Aug 1, 2023

"""
This file contains the definition of the class 'Song', which is used to represent a song with its various attributes.
The class is designed to be used in a playlist management system, where it will allow for the storage, display, and manipulation of song data.
"""

class Song:
    """
    The 'Song' class is used to represent a song with its various attributes such as rank, artist, title, length, and year.
    It includes methods to initialize a song and represent it as a string.
    """

    def __init__(self, rank, artist, title, length, year):
        """
        Initialize a Song instance.

        Args:
            rank (int): The rank of the song.
            artist (str): The artist of the song.
            title (str): The title of the song.
            length (Time): The length of the song.
            year (int): The release year of the song.
        """
        self.rank = rank
        self.artist = artist
        self.title = title
        self.length = length  # This should be a Time object
        self.year = year
        
    def __str__(self):
        """
        The string representation method for the 'Song' class. 
        Returns a formatted string that displays the song's rank, artist, title, length, and year.
        """
        return f""""{str(self.rank):>3} {self.artist:<20} {self.title:<30} {str(self.length):<5} {str(self.year):>4}"""
