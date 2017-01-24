"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app. Code is from Flask-SQLAlchemy
    documentation."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """
        # :github is a placeholder since that's all that will change between queries
        # No need to include a semicolon at the end of the string
        # QUERY is in uppercase because it'll be a constant variable

    # Gives :github placeholder an actual value from value passed to the function.
    # Sort of like a % substitution operator in Python
    # Execute the query:
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()  # Method that returns just one row
    # Unpacking tuple from .fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
            INSERT INTO students
                VALUES (:first_name, :last_name, :github)
            """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})

    db.session.commit()  # Inserting rows puts you in a transaction,
                         # so have to commit before changes can be implemented

    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
            SELECT *
            FROM projects
            WHERE title = :title
            """

    db.session.commit()

    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()

    print "Project Title: %s. \nDescription: %s." % (row[1], row[2])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
            SELECT grade
            FROM grades
            WHERE student_github = :github AND project_title = :title
            """

    db.session.commit()

    db_cursor = db.session.execute(QUERY, {'title': title,
                                           'github': github})
    row = db_cursor.fetchone()

    print "Grade = %s." % row[0]


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """
            UPDATE grades
                SET grade = :grade
            WHERE student_github = :github AND project_title = :title
            """

    db.session.execute(QUERY, {'github': github,
                               'title': title,
                               'grade': grade})

    db.session.commit()

    print "%s's project, %s, has been assigned a grade of %s." % (github,
                                                                  title,
                                                                  grade)



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project_by_title":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_grade_by_github_title":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."

if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()  # Calls close method on the connection upon quitting program
