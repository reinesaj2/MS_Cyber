# playlist.py - a class that represents a playlist of songs
# Author: Abraham Reines
# Created: Aug 1, 2023

"""
This file contains the definition of the class 'Playlist', which is used to represent a playlist of songs.
The class is designed to be used in a playlist management system, where it will allow for the storage, display, and manipulation of playlists.
"""

import sys
import os
from song import Song
from importlib.machinery import SourceFileLoader  # Import SourceFileLoader for dynamic module loading

# Dynamically loading the Time class from the time module
Time = SourceFileLoader('Time', os.path.join(sys.path[0], 'time.py')).load_module().Time

class Playlist:
    def __init__(self, name, songs=None):
        """
        Initialize a new Playlist instance.

        Args:
            name (str): The name of the playlist.
            songs (list[Song], optional): A list of Song objects to add to the playlist initially. Defaults to None.
        """
        self.name = name
        self.songs = songs if songs is not None else []

    def __str__(self):
        """
        Return a string representation of the Playlist instance, formatted as a list of songs.
        Each song is represented by its own string representation.

        Returns:
            str: A string representation of the Playlist instance.
        """
        playlist_str = "\n".join(str(song).lstrip('\"') for song in self.songs)
        return playlist_str

    def add_song(self, song=None):
        """
        Add a song to the playlist. If no song is provided, prompt the user for song details.

        Args:
            song (Song, optional): A Song instance to add to the playlist. Defaults to None.
        """
        if song is None:
            rank = input("Enter song rank: ")
            artist = input("Enter artist name: ")
            title = input("Enter song title: ")
            length = input("Enter song length (MM:SS): ")
            year = input("Enter song release year: ")
            song = Song(rank, artist, title, Time(length), year)
        self.songs.append(song)

    def del_song(self, title=None):
        """
        Delete a song from the playlist by title. If no title is provided, prompt the user for the title.

        Args:
            title (str, optional): The title of the song to delete. Defaults to None.
        """
        if title is None:
            title = input("Enter title of song to delete: ")
        song = next((song for song in self.songs if song.title == title), None)
        if song is not None:
            self.songs.remove(song)

    def get_choice(self, max_choice):
        """
        Prompt the user for a choice, an integer between 1 and max_choice.

        Args:
            max_choice (int): The maximum valid choice.

        Returns:
            int: The user's choice.
        """
        ch = ''
        while not ch.isdigit() or int(ch) < 1 or int(ch) > max_choice:
            ch = input('Choice: ')
        return int(ch)

    def sort(self):
        """
        Sort the songs in the playlist based on a user's choice of attribute.
        """
        choice = self.get_choice(5)
        fields = ['rank', 'title', 'artist', 'length', 'year']
        if fields[choice - 1] == 'rank' or fields[choice - 1] == 'year':
            self.songs.sort(key=lambda song: (int(getattr(song, fields[choice - 1])), song.rank))
        else:
            self.songs.sort(key=lambda song: (getattr(song, fields[choice - 1]), song.rank))

    
    def search(self, artist=None):
        """
        Search the playlist for songs by a certain artist. If no artist is provided, prompt the user for the artist's name.

        Args:
            artist (str, optional): The name of the artist to search for. Defaults to None.

        Returns:
            list[Song]: A list of Song instances by the artist.
        """
        if artist is None:
            artist = input("Enter artist name to search: ")
        found = [song for song in self.songs if song.artist == artist]
        for song in found:
            print(song)

    def print_songs(self):
        """
        Print all the songs in the playlist, each on a new line.
        """
        for song in self.songs:
            print(song)

    @property
    def duration(self):
        """
        Calculate the total duration of all the songs in the playlist.

        Returns:
            Time: A Time instance representing the total duration.
        """
        total_minutes = sum(song.length.minutes for song in self.songs)
        total_seconds = sum(song.length.seconds for song in self.songs)
        return Time(total_minutes + total_seconds // 60, total_seconds % 60)
