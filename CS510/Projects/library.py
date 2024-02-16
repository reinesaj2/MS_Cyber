#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 11:00:45 2023

@author: abrahamreines
"""

# library.py - manage a library's collection of books using a list
# Author:

# Collection1 is your library's collection. It starts out empty.
collection1 = []

# Collection2 is another library's collection.
collection2 = [
    ['Emma', 'Jane Austen'],
    ['Frankenstein', 'Mary Shelley'],
    ['Wuthering Heights', 'Emily Bronte'],
    ['Moby Dick', 'Herman Melville'],
    ['Oliver Twist', 'Charles Dickens'],
    ['The Adventures of Huckleberry Finn', 'Mark Twain'],
    ['Heart of Darkness', 'Joseph Conrad'],
    ['Ulysses', 'James Joyce'],
    ['Animal Farm', 'George Orwell'],
    ['Oliver Twist', 'Charles Dickens'],
    ['The Great Gatsby', 'F. Scott Fitzgerald'],
    ['Brave New World', 'Aldous Huxley'],
    ['Frankenstein', 'Mary Shelley']
]

# Collection3 is a third library's collection.
collection3 = [
    ['The Grapes of Wrath', 'John Steinbeck'],
    ['1984', 'George Orwell'],
    ['The Adventures of Huckleberry Finn', 'Mark Twain'],
    ['Ulysses', 'James Joyce'],
    ['Animal Farm', 'George Orwell'],
    ['The Catcher in the Rye', 'JD Salinger'],
    ['Frankenstein', 'Mary Shelley'],
    ['Lolita', 'Vladimir Nabokov'],
    ['Heart of Darkness', 'Joseph Conrad'],
    ['To Kill a Mockingbird', 'Harper Lee'],
    ['Ulysses', 'James Joyce'],
    ['The Great Gatsby', 'F. Scott Fitzgerald'],
    ['The Bell Jar', 'Sylvia Plath'],
    ['Brave New World', 'Aldous Huxley'],
    ['Song of Solomon', 'Toni Morrison']
]


def print_menu():
    print('1. Display all the books currently in your library')
    print('2. Add a book to your library')
    print('3. Remove a book from your library')
    print('4. Search for books in your library')
    print('5. Import books from other libraries')
    print('6. Exit')


def display_books(collection):
    if not collection:
        print("Your library is empty.")
    else:
        print("Books in your library:")
        for book in collection:
            print(f"Title: {book[0]}, Author: {book[1]}")


def add_book(collection):
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    book = [title, author]

    if book in collection:
        print("The book already exists in your library.")
    else:
        collection.append(book)
        collection.sort(key=lambda x: x[0])
        print("The book has been added to your library.")


def remove_book(collection):
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    book = [title, author]

    if book in collection:
        collection.remove(book)
        print("The book has been removed from your library.")
    else:
        print("The book does not exist in your library.")


def search_books(collection):
    search_field = input("Search by (1) Title or (2) Author: ")
    search_string = input("Enter the search string: ")

    matches = []
    for book in collection:
        if search_field == "1" and search_string.lower() in book[0].lower():
            matches.append(book)
        elif search_field == "2" and search_string.lower() in book[1].lower():
            matches.append(book)

    if matches:
        print("Matching books:")
        for book in matches:
            print(f"Title: {book[0]}, Author: {book[1]}")
    else:
        print("No matches found.")


def import_books(collection):
    new_books = 0

    for book in collection2 + collection3:
        if book not in collection:
            collection.append(book)
            new_books += 1

    collection.sort(key=lambda x: x[0])
    print(f"{new_books} new books have been imported into your library.")


print("Welcome to your library!")

while True:
    print_menu()
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        display_books(collection1)
    elif choice == "2":
        add_book(collection1)
    elif choice == "3":
        remove_book(collection1)
    elif choice == "4":
        search_books(collection1)
    elif choice == "5":
        import_books(collection1)
    elif choice == "6":
        print("Thank you for using the library. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")