import dbsystem
import questionary
from tabulate import tabulate
from style import *


def habit_exists(db, habit_name):
    """
    Checks if a habit exists in the database

    Parameters
    ----------
    db : sqlite3.connect()
        Connection to the database
    habit_name : str
        Name of the habit

    Returns
    -------
    bool
        true if the habit exists, false otherwise
    """
    cursor = db.cursor()
    cursor.execute(f"SELECT * from habits WHERE habit_name = '{habit_name}'")
    if(cursor.fetchone() is not None):
        return True
    else:
        return False
    
def get_habit_name():
    """
    Prompts the user to enter the name of the habit

    Returns
    -------
    str
        the name of the habit
    """
    db = dbsystem.connect_db()
    check = False
    while(not check):
        habit_name = questionary.text("Please Enter the Name of Your Habit:",
                   validate=lambda name: True if len(name) > 1
                   else "Please enter a valid name", style=custom_style_fancy).ask()
        check = habit_exists(db, habit_name)
        if(check):
            print(f"\n{YELLOW}****{habit_name} already exists. Please enter a different habit.****{END}\n")
            check = False
        else:
            check = True
    return habit_name

def get_habit_periodicity():
    """
    Prompts the user to select the periodicity of the habit

    Returns
    -------
    str
        the periodicity of the habit
    """
    habit_periodicity = questionary.select(
            "Please select the periodicity:",
            choices = [
                "Daily",
                "Weekly",
                "Monthly",
                "Yearly",
            ], style=custom_style_fancy
            ).ask()
    return habit_periodicity

def get_habit_duration():
    """
    Prompts the user to enter the duration of the habit
    The user can leave it blank

    Returns
    -------
    str
        the duration of the habit
    """
    habit_duration = questionary.text("Please specify the duration.(e.g. 30 days, 2 weeks, 6 months, etc)", style=custom_style_fancy).ask()
    return habit_duration

def get_habits_only(db):
    """
    Gets all habit names from the database

    Returns
    -------
    list
        Return the names of all habits
    """
    cursor = db.cursor()
    cursor.execute("SELECT habit_name FROM habits;")
    habits_only = cursor.fetchall()
    return [i[0] for i in set(habits_only)] if len(habits_only) > 0 else None