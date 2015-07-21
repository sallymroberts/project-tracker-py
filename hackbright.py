"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT title, description 
        FROM projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,)) 
    row = db_cursor.fetchone()
    print "Project Title: %s\n Project description: %s" % (
        row[0], row[1])



def get_grade_by_github_title(student_github, project_title):
    """Print grade student received for a project."""
    QUERY = """
        SELECT student_github, project_title, grade
        FROM grades
        WHERE student_github = ? 
        AND project_title = ?
        """

    db_cursor.execute(QUERY, (student_github, project_title))
    row = db_cursor.fetchone()
    print "Github account: %s \nProject title: %s\nGrade: %s" % (
        row[0], row[1], row[2])



def assign_grade(student_github, project_title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
    INSERT INTO Grades 
    VALUES (?, ?, ?)"""
    db_cursor.execute(QUERY, (student_github, project_title, grade))
    db_connection.commit()
    print "Successfully added: %s, %s \nGrade: %s" % (student_github, project_title, grade)




def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        print "After accepting raw input"
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "student_grade":
            student_github = args[0]
            project_title = args[1]
            get_grade_by_github_title(student_github, project_title)

        elif command == "add_grade":
            student_github, project_title, grade = args
            assign_grade(student_github, project_title, grade)





if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
