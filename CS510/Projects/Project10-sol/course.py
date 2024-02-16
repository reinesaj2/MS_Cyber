"""
File: course.py
Author: Abraham Reines
Created: 11:43:04 July 25, 2023 
Description: This script defines the Course class.
"""

class Course:
    """A class that represents a course.

    Attributes:
    title (str): The title of the course.
    roster (list): A list of Student objects that are enrolled in the course.
    """
    def __init__(self, title):
        """Initialize a new Course object.

        Args:
        title (str): The title of the course.
        """
        self.title = title
        self.roster = []

    @classmethod
    def create_new_course(cls, title):
        """Create a new Course object.

        This class method creates a new Course object using the provided title.

        Args:
        title (str): The title of the course.

        Returns:
        Course: A new Course object.
        """
        return cls(title)

    def add_student(self, student):
        """Add a student to the course.

        This method adds a Student object to the roster of the Course object on which it is called.

        Args:
        student (Student): A Student object.
        """
        self.roster.append(student)

    def course_size(self):
        """Get the size of the course.

        This method returns the number of students in the Course object on which it is called.

        Returns:
        int: The number of students in the course.
        """
        return len(self.roster)

    def print_roster(self):
        """Print the roster of the course.

        This method prints the first name, last name, and grade of each student in the Course object on which it is called.
        """
        for student in self.roster:
            print(f'{student.first} {student.last}: {student.grade}')

    def find_top_grade(self):
        """Find the top grade in the course.

        This method finds and returns the highest grade among all students in the Course object on which it is called.

        Returns:
        float: The top grade in the course.
        """
        return max(student.grade for student in self.roster)

    def find_average(self):
        """Find the average grade in the course.

        This method calculates and returns the average grade of all students in the Course object on which it is called.

        Returns:
        float: The average grade in the course.
        """
        return sum(student.grade for student in self.roster) / self.course_size()

    def find_bottom_grade(self):
        """Find the bottom grade in the course.

        This method finds and returns the lowest grade among all students in the Course object on which it is called.

        Returns:
        float: The bottom grade in the course.
        """
        return min(student.grade for student in self.roster)
