"""
File: student.py
Author: Abraham Reines
Created: 11:43:15 July 25, 2023 
Description: This script defines the Student class.
"""

class Student:
    """A class that represents a student.

    Attributes:
    first (str): The first name of the student.
    last (str): The last name of the student.
    grade (float): The grade of the student.
    """
    def __init__(self, first, last, grade):
        """Initialize a new Student object.
        Args:
        The first name of the student.
        The last name of the student.
        The grade of the student.
        """
        self.first = first
        self.last = last
        self.grade = grade

    @classmethod
    def create_new_student(cls, first, last, grade):
        """Create a new Student object.

        This class method creates a new Student object using the provided
        first name, last name, and grade.

        Returns:
        Student: A new Student object.
        """
        return cls(first, last, grade)

