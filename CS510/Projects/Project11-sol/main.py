# Author: Abraham Reines
# Created: Aug 1, 2023
"""
This is the main script for the playlist management system.
It includes functions to import data, print the menu, get user choice, 
add and delete songs, sort the playlist, and search for songs by artist.
It uses the 'Playlist', 'Song', and 'Time' classes to perform these operations.
"""

# Importing necessary modules and classes
import sys
import os
import random
from playlist import Playlist  # Import Playlist class from playlist module
from song import Song  # Import Song class from song module
from importlib.machinery import SourceFileLoader  # Import SourceFileLoader for dynamic module loading

# Dynamically loading the Time class from the time module
Time = SourceFileLoader('Time', os.path.join(sys.path[0], 'time.py')).load_module().Time

# Function to import song data from a file and add to playlists
def import_data(big_playlist, small_playlist):
    """
    Imports song data from the 'RollingStone2004List.txt' file and populates the provided playlists.
    Every song is added to the big playlist. 1 in 50 songs (randomly selected) are also added to the small playlist.
    
    Args:
        big_playlist (Playlist): The main playlist to which all songs will be added.
        small_playlist (Playlist): A smaller playlist to which some songs will be added.
    """
    with open('RollingStone2004List.txt', 'r') as file:
        for line in file:
            rank, artist, title, length, year = line.strip().split('\t')
            song = Song(rank, artist, title, Time(length), year)
            big_playlist.add_song(song)
            if random.randint(1, 50) == 1:
                small_playlist.add_song(song)

# Function to print the main menu options
def print_menu():
    """
    Prints the main menu options for the user.
    """
    print('1. Display small playlist info')
    print('2. Add a song to the small playlist')
    print('3. Delete a song from the small playlist')
    print('4. Sort small playlist')
    print('5. Search big playlist by artist')
    print('6. Exit')

# Function to get the user's choice from the menu
def get_choice(max_choice):
    """
    Prompt the user for a choice between 1 and max_choice, inclusive.
    
    Args:
        max_choice (int): The maximum valid choice.

    Returns:
        int: The user's choice.
    """
    ch = ''
    while not ch.isdigit() or int(ch) < 1 or int(ch) > max_choice:
        ch = input('Choice: ')
    return int(ch)

def sort_menu():
    """
    Prints the sort menu options for the user.
    """
    print('Sort by:')
    print('1. Rank')
    print('2. Title')
    print('3. Artist')
    print('4. Length')
    print('5. Year')

# Main script function
if __name__ == '__main__':
    big_playlist = Playlist("Big Playlist")
    small_playlist = Playlist("Small Playlist")
    import_data(big_playlist, small_playlist)
    choice = 0
    while choice != 6:
        print_menu()
        choice = get_choice(6)
        if choice == 1:
            print(small_playlist)
            print('\n')
        elif choice == 2:
            small_playlist.add_song()
            print('\n')
            print(small_playlist)
            print('\n')
        elif choice == 3:
            small_playlist.del_song()
            print('\n')
            print(small_playlist)
            print('\n')
        elif choice == 4:
            sort_menu()
            small_playlist.sort()
            print('\n')
            print(small_playlist)
            print('\n')
        elif choice == 5:
            print(big_playlist.search())
