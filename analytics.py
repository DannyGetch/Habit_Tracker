from dbsystem import connect_db
from tabulate import tabulate
import getter
import questionary
from style import *

HEADERS = ['Habit', 'Periodicity', 'Duration', 'Streak', 'Streak Type', 'Last Completed', 'Date Created']

def connector():
    """
    The connector function is used to connect to the database.
        It returns a cursor object that can be used for querying.
    
    Parameters
    ----------
    
    Returns
    -------
    
        A cursor object
    """
    db = connect_db()
    cursor = db.cursor()
    return cursor

cursor = connector()

def show_daily_habits():
    """
    The show_daily_habits function prints a table of all habits that are marked as daily.
    """
    data = cursor.execute("SELECT * FROM habits WHERE Periodicity = 'Daily'").fetchall()
    print_table(data, HEADERS)

def show_weekly_habits():
    data = cursor.execute("SELECT * FROM habits WHERE Periodicity = 'Weekly'").fetchall()
    print_table(data, HEADERS)

def show_monthly_habits():
    """
    The show_monthly_habits function prints a table of all habits that are marked as monthly.
    """
    data = cursor.execute("SELECT * FROM habits WHERE Periodicity = 'Monthly'").fetchall()
    print_table(data, HEADERS)

def show_yearly_habits():
    """
    The show_yearly_habits function prints a table of all habits that are marked as yearly.
    """
    data = cursor.execute("SELECT * FROM habits WHERE Periodicity = 'Yearly'").fetchall()
    print_table(data, HEADERS)

def show_all_habits():
    """
    The show_all_habits function prints a table of all habits in the database.
    """
    data = cursor.execute("SELECT * FROM habits").fetchall()
    print_table(data, HEADERS)

def print_table(data, HEADERS):
    """
    The print_table function takes two arguments:
        1. data - a list of lists containing the data to be printed in table format
        2. HEADERS - a list of strings that will serve as the headers for each column
    
    Parameters
    ----------
        data
            Pass in the data to be printed
        HEADERS
            Print the headers of the table
    """
    print(tabulate(data, HEADERS, tablefmt="outline"))

def completed_dates():
    """
    The completed_dates function is used to display the first and last time a habit was completed, as well as the current streak.
    The user will be prompted to select a habit from their list of habits.
    """
    db = connect_db()
    habits_only = getter.get_habits_only(db)
    if(habits_only is not None):
        habit = questionary.select(
            "Please select the habit:",
            choices=sorted(habits_only), style=custom_style_fancy
        ).ask()
        cursor = db.cursor()
        data = cursor.execute(f"SELECT * FROM log WHERE habit_name = '{habit}'").fetchall()
        headers = ['Habit', 'First Completed on', 'Last Completed on', 'Streak', 'Streak Type']
        print(tabulate(data, headers, tablefmt="outline"))
    else:
        print(f"\n{RED}****No Habits in the Database****{END}\n")

def currently_tracked_habits():
    """
    The currently_tracked_habits function prints a table of all habits that are currently being tracked.
    It does this by querying the database for all habits where streak > 0, and then printing the results in a table.
    """
    data = cursor.execute(f"SELECT * FROM habits WHERE streak > 0;").fetchall()
    print_table(data, HEADERS)

def longest_daily_habit_streak():
    """
    The longest_daily_habit_streak function prints the longest daily habit streak.
    """
    data = cursor.execute(f"SELECT *  FROM habits WHERE Periodicity = 'Daily' AND streak = (SELECT MAX(streak) FROM habits WHERE Periodicity = 'Daily');").fetchall()
    print_table(data, HEADERS)

def longest_weekly_habit_streak():
    """
    The longest_weekly_habit_streak function prints the longest weekly habit streak.
    """
    data = cursor.execute(f"SELECT *  FROM habits WHERE Periodicity = 'Weekly' AND streak = (SELECT MAX(streak) FROM habits WHERE Periodicity = 'Weekly');").fetchall()
    print_table(data, HEADERS)

def longest_monthly_habit_streak():
    """
    The longest_monthly_habit_streak function prints the longest monthly habit streak.
    """
    data = cursor.execute(f"SELECT *  FROM habits WHERE Periodicity = 'Monthly' AND streak = (SELECT MAX(streak) FROM habits WHERE Periodicity = 'Monthly');").fetchall()
    print_table(data, HEADERS)

def longest_yearly_habit_streak():
    """
    The longest_yearly_habit_streak function prints the longest yearly habit streak.
    """
    data = cursor.execute(f"SELECT *  FROM habits WHERE Periodicity = 'Yearly' AND streak = (SELECT MAX(streak) FROM habits WHERE Periodicity = 'Yearly');").fetchall()
    print_table(data, HEADERS)

def longest_ever_streak():
    """
    The longest_ever_streak function is used to find the longest streak of a habit.
    It takes in no arguments and returns nothing. It uses the getter module to get all habits from the database, then asks for user input on which habit they want to see their longest streak for. Then it queries that data from the database and prints it out using tabulate.
    """
    db = connect_db()
    habits_only = getter.get_habits_only(db)
    if(habits_only is not None):
        habit = questionary.select(
            "Please select the habit:",
            choices=sorted(habits_only), style=custom_style_fancy
        ).ask()
        cursor = db.cursor()
        data = cursor.execute(f"SELECT * FROM log WHERE habit_name = '{habit}' AND streak = (SELECT MAX(streak) FROM log WHERE habit_name = '{habit}')").fetchall()
        headers = ['Habit', 'First Completed on', 'Last Completed on', 'Streak', 'Streak Type']
        print(tabulate(data, headers, tablefmt="outline"))
    else:
        print(f"\n{RED}****No Habits in the Database****{END}\n")

def inactivity():
    """
    The inactivity function is used to display the inactivity log of a habit.
    The user will be prompted to select a habit from the list of habits in the database.
    Once selected, all inactive dates and streaks for that habit will be displayed.
    """
    db = connect_db()
    habits_only = getter.get_habits_only(db)
    if(habits_only is not None):
        habit = questionary.select(
            "Please select the habit:",
            choices=sorted(habits_only), style=custom_style_fancy
        ).ask()
        cursor = db.cursor()
        data = cursor.execute(f"SELECT * FROM inactive_log WHERE habit_name = '{habit}'").fetchall()
        headers = ['Habit', 'First Inactive Date', 'Last Inactive Date', 'Inactive Streak', 'Streak Type']
        print(tabulate(data, headers, tablefmt="outline"))

    else:
        print(f"\n{RED}****No Habits in the Database****{END}\n")

def longest_ever_inactivity():
    """
    The longest_ever_inactivity function is used to find the longest inactive streak for a habit.
    It will ask the user to select a habit from their list of habits, and then it will print out
    the first date that they were inactive, the last date that they were inactive, how many days in 
    a row they were inactive for (inactive_streak), and whether or not this was an active streak or 
    an incomplete streak.
    """
    db = connect_db()
    habits_only = getter.get_habits_only(db)
    if(habits_only is not None):
        habit = questionary.select(
            "Please select the habit:",
            choices=sorted(habits_only), style=custom_style_fancy
        ).ask()
        cursor = db.cursor()
        data = cursor.execute(f"SELECT * FROM inactive_log WHERE habit_name = '{habit}' AND inactive_streak = (SELECT MAX(inactive_streak) FROM inactive_log WHERE habit_name = '{habit}')").fetchall()
        headers = ['Habit', 'First Inactive Date', 'Last Inactive Date', 'Inactive Streak', 'Streak Type']
        print(tabulate(data, headers, tablefmt="outline"))

    else:
        print(f"\n{RED}****No Habits in the Database****{END}\n")