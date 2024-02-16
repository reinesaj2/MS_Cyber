"""
File: main.py
Author: Abraham Reines
Created: 11:42:28 July 25, 2023 
Description: This script provides a command-line interface for interacting with courses and students.
"""

from course import Course
from student import Student
import os
from pathlib import Path

def import_data(directory):
    """Import data from data files.

    This function reads each file in the data directory and creates a Course object whose title is the name of the file.
    It then reads each line of the file, creates a Student object from that line, and adds it to the Course's roster.
    It then adds the Course object to the list of courses.

    Args:
    courses (list): A list to which Course objects are added.
    """
    courses = []
    for filename in os.listdir(directory):
        # Check if the file is a text file (not a directory or a system file)
        if not filename.startswith('.'):
            # Construct full path to the file
            full_path = os.path.join(directory, filename)
            # Open the file with 'latin-1' encoding
            with open(full_path, 'r', encoding='latin-1') as file:
                # Create a new course with the filename (without .txt) as the course name
                course = Course(filename.replace('.txt', ''))
                # Iterate over each line in the file
                for line in file.readlines():
                    # Split each line into first name, last name and grade
                    first, last, grade = line.strip().split(" ")
                    # Create a new student and add it to the course
                    student = Student(first, last, float(grade))
                    course.add_student(student)
                # Add the course to the list of courses
                courses.append(course)
    return courses

# Main function
def main():
    """The main function of the program.

    This function creates a new, empty list of courses and calls the import_data() function.
    It then enters a loop where it prompts the user for a choice, checks that it is valid, and then performs the selected option.
    The loop continues until the user chooses to exit the program.
    """
    # Import data
    
    # Get the current script's directory
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    
    # Navigate to the parent directory
    parent_dir = script_dir.parent
    
    # Append the 'data' directory to the parent directory
    data_dir = parent_dir / 'Project10-sol/data'
    
    # Now you can import data from the 'data' directory
    courses = import_data(str(data_dir))

    # User interface loop
    while True:
        print("\nMain Menu:")
        print("1. Display class roster")
        print("2. Display class statistics (high, low, and average grade)")
        print("3. Display student grades (with GPA)")
        print("4. Display students on double secret probation")
        print("5. Display valedictorians")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            """This option prompts the user for a course name and then prints out the roster for that course."""
            course_name = input("Enter course name: ")
            found_course = False
            for course in courses:
                if course.title == course_name:
                    course.print_roster()
                    found_course = True
                    break
            if not found_course:
                print("Course not found.")
                    
                
        elif choice == '2':
            """This option prompts the user for a course name and then prints out the highest grade, lowest grade, 
            and average grade in that course."""
            course_name = input("Enter course name: ")
            found_course = False
            for course in courses:
                if course.title == course_name:
                    high = course.find_top_grade()
                    avg = course.find_average()
                    low = course.find_bottom_grade()
                    print(f'High grade: {high}, Average grade: {avg}, Low grade: {low}')
                    found_course = True
                    break
            if not found_course:
                print("Course not found.")
                    
                
        elif choice == '3':
            """This option prompts the user for a student name and then prints out each course that student is in, 
            their grade in each course, and their overall GPA."""
            student_name = input("Enter student name: ")
            total_grades = 0
            total_courses = 0
            for course in courses:
                for student in course.roster:
                    if f'{student.first} {student.last}' == student_name:
                        print(f'Course: {course.title}, Grade: {student.grade}')
                        total_grades += student.grade
                        total_courses += 1
            if total_courses > 0:
                print(f'GPA: {total_grades/total_courses}')
            else:
                print("Student not found.")
                
                
        elif choice == '4':
            """This option prints out all students who are on double secret probation (GPA <= 1.0)."""
            student_grades = {}
            for course in courses:
                for student in course.roster:
                    student_full_name = f"{student.first} {student.last}"
                    if student_full_name not in student_grades:
                        student_grades[student_full_name] = [student.grade]
                    else:
                        student_grades[student_full_name].append(student.grade)
            for student_name, grades in student_grades.items():
                gpa = sum(grades) / len(grades)
                if gpa <= 1.0:
                    print(f"{student_name} is on double secret probation.")


        elif choice == '5':
            """This option prints out the student or students who are the valedictorian(s). 
            Valedictorians have the highest GPA of all students."""
            student_grades = {}
            for course in courses:
                for student in course.roster:
                    student_full_name = f"{student.first} {student.last}"
                    if student_full_name not in student_grades:
                        student_grades[student_full_name] = [student.grade]
                    else:
                        student_grades[student_full_name].append(student.grade)
            highest_gpa = 0
            valedictorians = []
            for student_name, grades in student_grades.items():
                gpa = sum(grades) / len(grades)
                if gpa > highest_gpa:
                    highest_gpa = gpa
                    valedictorians = [student_name]
                elif gpa == highest_gpa:
                    valedictorians.append(student_name)
            print("Valedictorians (highest GPA):")
            for valedictorian in valedictorians:
                print(f"{valedictorian}: {highest_gpa}")

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main()