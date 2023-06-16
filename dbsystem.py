import datetime
import sqlite3
import questionary
from tabulate import tabulate
from style import *
from log import Log, InactiveLog

def connect_db(database_name="database.db"):
    """
    The connect_db function connects to the database and creates a table if it doesn't exist.
        Args:
            database_name (str): The name of the database file. Defaults to database.db
    
    Parameters
    ----------
        database_name
            Specify the name of the database that we want to connect to
    
    Returns
    -------
    
        A database connection object
    """
    db = sqlite3.connect(database_name)
    create_table(db)
    create_log_table(db)
    create_inactive_log_table(db)
    return db

def create_table(db):
    """
    The create_table function creates a table called habits.
        
    
    Parameters
    ----------
        db
            Connect to the database
    
   
    """
    cursor = db.cursor()
    #cursor.execute("DROP TABLE habits;")
    #cursor.execute("DROP TABLE log;")
    cursor.execute("CREATE TABLE IF NOT EXISTS habits (habit_name VARCHAR(30), periodicity VARCHAR(10), duration VARCHAR(30), streak VARCHAR(15), streak_type VARCHAR(10), date_last_completed Date, created_on Date);")
    db.commit()

def add_habit(db, habit_name, habit_periodicity, habit_duration, streak, streak_type, date_last_completed, current_time):
    """
    The add_habit function adds a habit to the habits table in the database.
        
    
    Parameters
    ----------
        db
            Connect to the database
        habit_name
            Identify the habit
        habit_periodicity
            Determine how often the habit should be completed
        habit_duration
            Determine how long the user wants to do the habit for
        streak
            Store the current streak of the habit in terms of days, or weeks, or months, or years
        streak_type
            Determine whether the streak is in terms of days, weeks, months or years
        date_last_completed
            Keep track of the last time a habit was completed
        current_time
            Store the time when the habit was added to the table
    """
    cursor = db.cursor()
    cursor.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)", (habit_name, habit_periodicity, habit_duration, streak, streak_type, date_last_completed, current_time))
    db.commit()
    print(f"\n{GREEN}****Successfully added {habit_name}****{END}\n")



def delete_habit(db, habit):
    """
    The delete_habit function takes in a database and a habit name as parameters.
    It then prompts the user to confirm that they want to delete the habit, and if so, deletes it from the habits table.
    
    Parameters
    ----------
        db
            Connect to the database
        habit
            Name of the habit to be deleted
    """
    prompt = questionary.text(f"Are you sure you want to delete \"{habit}\"? Y/N", style=custom_style_fancy).ask()
    if(prompt == "Y" or prompt == "y"):
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM habits WHERE habit_name = '{habit}';")
        cursor.execute(f"DELETE FROM log WHERE habit_name = '{habit}';")
        cursor.execute(f"DELETE FROM inactive_log WHERE habit_name = '{habit}';")
        db.commit()
        print(f"\n{GREEN}******Successfully deleted {habit}******{END}\n")
    else:
        print(f"\n{RED}*****{habit} is not deleted!*****{END}\n")
    

def first_time_check_off(db, habit_name, current_completed_time, streak_type):
    """
    The first_time_check_off function is used to check off a habit for the first time.
    It takes in the database, habit name, current completed time and streak type as parameters.
    The function then sets the first_completed_time variable equal to current_completed_time.
    Then it updates date last completed with current completed time and streak with 1 in habits table where habit name equals 
    the parameter passed into this function (habit name). It commits these changes to the database and then creates a Log object 
    with all of its parameters being set equal to their respective variables that were just updated or created.
    
    Parameters
    ----------
        db
            Connect to the database
        habit_name
            Select the habit from the database
        current_completed_time
            Keep track of the current time a habit is completed
        streak_type
            Determine type of the streak
    """
    cursor = db.cursor()
    first_completed_time = current_completed_time
    cursor.execute(f"UPDATE habits SET date_last_completed = '{current_completed_time}' WHERE habit_name = '{habit_name}';")
    cursor.execute(f"UPDATE habits SET streak = 1 WHERE habit_name = '{habit_name}';")
    db.commit()
    streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
    logger = Log(habit_name, first_completed_time, current_completed_time, streak, streak_type)
    logger.add()

def check_off(db, habit_name, current_completed_time, last_completed, streak_type):
    """
    The check_off function takes in the database, habit name, current completed time, last completed date and streak type.
    It then updates the habits table with the new date_last_completed and increments streak by 1. It also creates a Log object
    and calls its add method to log this completion.
    
    Parameters
    ----------
        db
            Connect to the database
        habit_name
            Identify the habit that is being checked off
        current_completed_time
            Keep track of the current time a habit is completed
        last_completed
            Keep track of the last time a habit was completed
        streak_type
            Determine whether the streak is a daily, weekly or monthly streak
    """
    cursor = db.cursor()
    first_completed_time = cursor.execute(f"SELECT first_completed_time FROM log WHERE last_completed_date = '{last_completed}'").fetchone()[0]
    cursor.execute(f"UPDATE habits SET date_last_completed = '{current_completed_time}' WHERE habit_name = '{habit_name}';")
    cursor.execute(f"UPDATE habits SET streak = streak + 1 WHERE habit_name = '{habit_name}';")
    db.commit()
    streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
    logger = Log(habit_name, first_completed_time, current_completed_time, streak, streak_type)
    logger.add()

def reset_check_off(db, habit_name, current_completed_time, streak_type):
    """
    The reset_check_off function is used to reset the streak of a habit when it has been completed.
    It takes in three arguments: db, habit_name, and current_completed_time.
    The first argument is the database that we are using for this program. The second argument is the name of the habit that we want to reset its streak for. The third argument is a string representing today's date.
    
    Parameters
    ----------
        db
            Connect to the database
        habit_name
            Find the habit in the database
        current_completed_time
            Keep track of the current time a habit is completed
        streak_type
            Determine type of the streak
    """
    cursor = db.cursor()
    cursor.execute(f"UPDATE habits SET date_last_completed = '{current_completed_time}' WHERE habit_name = '{habit_name}';")
    cursor.execute(f"UPDATE habits SET streak = 1 WHERE habit_name = '{habit_name}';")
    db.commit()
    logger = Log(habit_name, current_completed_time, current_completed_time, '1', streak_type)
    logger.add()
    db.commit()

def log_inactivity(habit_name, last_inactive_time, first_inactive_time, inactive_streak, inactive_streak_type):
    """
    The log_inactivity function takes in the following parameters:
        habit_name - The name of the habit that is being logged.
        last_inactive_time - The time at which the user was last inactive for this particular habit.
        first_inactive_time - The time at which the user became inactive for this particular habit. This will be used to calculate how long a streak has been going on, and when it started. 
        inactive_streak - How many days have passed since a user has done their activity? This will be calculated by subtracting first from last (last-first). 
    
    Parameters
    ----------
        habit_name
            Identify which habit is being logged
        last_inactive_time
            Store the time of the last inactive streak
        first_inactive_time
            Store the time of the first missed habit
        inactive_streak
            Determine how long the user has been inactive for
        inactive_streak_type
            Determine the inactive streak type
    """
    inactive_logger = InactiveLog(habit_name, last_inactive_time, first_inactive_time, inactive_streak, inactive_streak_type)
    inactive_logger.add()

def get_dates(last_completed, current_completed_time):
    """
    The get_dates function takes two arguments, last_completed and current_completed_time.
    The function converts the strings into datetime objects and returns them as d2 - d2.
    
    Parameters
    ----------
        last_completed
            Get the date of the last completed date
        current_completed_time
            Get the current date and time
    """
    d1 = datetime.datetime.strptime(last_completed, "%d/%m/%Y %H:%M").date()
    d2 = datetime.datetime.strptime(current_completed_time, "%d/%m/%Y %H:%M").date()
    return d1,d2
    
def mark_habit_done(db, habit_name):
    """
    The mark_habit_done function is used to mark a habit as completed.
    It takes in the database and the name of the habit that was completed.
    The function then checks if this is the first time that this habit has been marked as complete, or if it's not. 
    If it's not, then we check how long ago was it last marked as complete (in days/weeks/months/years). 
    If there are no gaps between completion dates, we update our streak count by 1 and print out a message saying so! 
    
    Parameters
    ----------
        db
            Connect to the database
        habit_name
            Identify the habit in the database
    
    """
    cursor = db.cursor()
    habit_periodicity = cursor.execute(f"SELECT periodicity FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
    last_completed = cursor.execute(f"SELECT date_last_completed FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
    current_completed_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if(habit_periodicity == "Daily"):
        streak_type = "day(s)"
        if(last_completed == None):
            first_time_check_off(db, habit_name, current_completed_time, streak_type)
            print(f"\n{GREEN}******Woooohooooooo! First day of the streak! Let's gooooo!*******{END}\n")

        else:
            d1, d2 = get_dates(last_completed, current_completed_time)
            diff = (d2 - d1).days

            if(diff == 0):
                print(f"\n{YELLOW}******You have already completed this habit on {last_completed}******{END}\n")
                print(f"\n{YELLOW}******Try again tomorrow!******{END}\n")
            elif(diff == 1):
                check_off(db, habit_name, current_completed_time, last_completed, streak_type)
                streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
                print(f"\n{GREEN}******You're doing great!*******{END}\n")
                print(f"\n******{GREEN}You have a new streak of {streak} day(s)!*******{END}\n")
            else:
                print(f"\n****{RED}You did not complete this habit for {diff} days!******{END}\n")
                print(f"\n****{RED}You have broken your streak, we're starting over!******{END}\n")
                log_inactivity(habit_name, last_completed, current_completed_time, diff, streak_type)
                reset_check_off(db, habit_name, current_completed_time, streak_type)

    elif(habit_periodicity == "Weekly"):
        streak_type = "week(s)"
        if(last_completed == None):
            first_time_check_off(db, habit_name, current_completed_time, streak_type)
            print(f"\n{GREEN}******Woooohooooooo! First week of the streak! Let's gooooo!*******{END}\n")
        else:
            d1, d2 = get_dates(last_completed, current_completed_time)
            monday1 = (d1 - datetime.timedelta(days=d1.weekday()))
            monday2 = (d2 - datetime.timedelta(days=d2.weekday()))
            diff = (monday2 - monday1).days / 7

            if(diff == 0):
                print(f"\n{YELLOW}******You have already completed this habit on {last_completed}******{END}\n")
                print(f"\n{YELLOW}******Try again next week!******{END}\n")
            elif(diff == 1):
                check_off(db, habit_name, current_completed_time, last_completed, streak_type)
                streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
                print(f"\n{GREEN}******You're doing great!*******{END}\n")
                print(f"\n{GREEN}******You have a new streak of {streak} week(s)!*******{END}\n")
            else:
                print(f"\n****{RED}You did not complete this habit for {diff} weeks!******{END}\n")
                print(f"\n****{RED}You have broken your streak, we're starting over!******{END}\n")
                log_inactivity(habit_name, last_completed, current_completed_time, diff, streak_type)
                reset_check_off(db, habit_name, current_completed_time, streak_type)
    elif(habit_periodicity == "Monthly"):
        streak_type = "month(s)"
        if(last_completed == None):
            first_time_check_off(db, habit_name, current_completed_time, streak_type)
            print(f"\n{GREEN}******Woooohooooooo! First month of the streak! Let's gooooo!*******{END}\n")
        else:
            d1, d2 = get_dates(last_completed, current_completed_time)
            month1 = d1.month
            month2 = d2.month
            diff = (month2 - month1)
            if(diff < 0):
                diff += 12

            if(diff == 0):
                print(f"\n{YELLOW}******You have already completed this habit on {last_completed}******{END}\n")
                print(f"\n{YELLOW}******Try again next month!******{END}\n")
            elif(diff ==  1):
                check_off(db, habit_name, current_completed_time, last_completed, streak_type)
                streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
                print(f"\n{GREEN}******You're doing great!*******{END}\n")
                print(f"\n{GREEN}******You have a new streak of {streak} month(s)!*******{END}\n")
            else:
                print(f"\n****{RED}You did not complete this habit for {diff} months!******{END}\n")
                print(f"\n{RED}****You have broken your streak, we're starting over!******{RED}\n")
                log_inactivity(habit_name, last_completed, current_completed_time, diff, streak_type)
                reset_check_off(db, habit_name, current_completed_time, streak_type)
    elif(habit_periodicity == "Yearly"):
        streak_type = "year(s)"
        if(last_completed == None):
            first_time_check_off(db, habit_name, current_completed_time, streak_type)
            print(f"\n{GREEN}******Woooohooooooo! First year of the streak! Let's gooooo!*******{END}\n")
        else:
            d1, d2 = get_dates(last_completed, current_completed_time)
            year1 = d1.year
            year2 = d2.year
            diff = year2 - year1

            if(diff == 0):
                print(f"\n{YELLOW}******You have already completed this habit on {last_completed}******{END}\n")
                print(f"\n{YELLOW}******Try again next year!******{END}\n")
            elif(diff == 1):
                check_off(db, habit_name, current_completed_time, last_completed, streak_type)
                streak = cursor.execute(f"SELECT streak FROM habits WHERE habit_name = '{habit_name}';").fetchone()[0]
                print(f"\n{GREEN}******You're doing great!*******{END}\n")
                print(f"\n{GREEN}******You have a new streak of {streak} year(s)!*******{END}\n")
            else:
                print(f"\n****{RED}You did not complete this habit for {diff} years!******{END}\n")
                print(f"\n{RED}****You have broken your streak, we're starting over!******{END}\n")
                log_inactivity(habit_name, last_completed, current_completed_time, diff, streak_type)
                reset_check_off(db, habit_name, current_completed_time, streak_type)


def update_habit(db, habit):
    """
    The update_habit function allows the user to update a habit's name, periodicity and duration.
    The function takes in two arguments: db (the database) and habit (the name of the habit that is being updated).
    It then asks for a new name for the selected habit, if no input is given it keeps the old one. It then asks for a new periodicity 
    and duration using questionary prompts. The function uses SQL queries to update all three values in both habits table and log table.
    
    Parameters
    ----------
        db
            Connect to the database
        habit
            Get the habit name from the user
    """
    new_name = questionary.text("Please type a new name for the selected habit (Just press enter if you want to keep the old name):", style=custom_style_fancy).ask()
    
    if(new_name == ""):
        new_name = habit

    new_periodicity = questionary.select("Please select a new periodicity for the selected habit:",
        choices = [
            "Daily",
            "Weekly",
            "Monthly",
            "Yearly"
            ], style=custom_style_fancy).ask()
    new_duration = questionary.text("Please type a new duration for the selected habit:", style=custom_style_fancy).ask()
    cursor = db.cursor()
    cursor.execute(f"UPDATE habits SET habit_name = '{new_name}' WHERE habit_name = '{habit}';")
    cursor.execute(f"UPDATE habits SET periodicity = '{new_periodicity}' WHERE habit_name = '{new_name}';")
    cursor.execute(f"UPDATE habits SET duration = '{new_duration}' WHERE habit_name = '{new_name}';")
    
    #Also update the log and inactive_log tables
    cursor.execute(f"UPDATE log SET habit_name = '{new_name}' WHERE habit_name = '{habit}';")
    cursor.execute(f"UPDATE inactive_log SET habit_name = '{new_name}' WHERE habit_name = '{habit}';")
    
    db.commit()
    print(f"\n{GREEN}****Habit successfully updated****{END}\n")

def clear_habits():
    """
    The clear_habits function is used to clear all habits from the database.
    It asks the user if they are sure, and then deletes all rows in both tables.
    """
    db = connect_db()
    choice = questionary.text("Are you sure? Y/N", style=custom_style_fancy).ask()
    if(choice == "Y" or choice == "y"):
        cursor = db.cursor()
        cursor.execute("DELETE FROM habits;")
        cursor.execute("DELETE FROM log;")
        cursor.execute("DELETE FROM inactive_log;")
        db.commit()
        print(f"\n{GREEN}********All habits have been removed********{END}\n")
    else:
        print(f"\n{RED}********No habits have been removed********{END}\n")

def create_log_table(db):
    """
    The create_log_table function creates a table in the database called log.
    The log table has 5 columns: habit_name, first_completed_time, last_completed_date, streak and streak type.
    Habit name is a string of up to 30 characters that describes the habit being tracked.
    First completed time is the date when you first started tracking this particular habit (i.e., when you created it).  It's stored as a Date object in Python and as an SQLite3 DATE object in your database file (habit-tracker-db).  This column will be used to calculate how long you
    
    Parameters
    ----------
        db
            Connect to the database
    """
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS log (habit_name VARCHAR(30), first_completed_time Date, last_completed_date Date, streak INT, streak_type VARCHAR(10));")
    db.commit()

def create_inactive_log_table(db):
    """
    The create_inactive_log_table function creates a table in the database that stores information about inactive streaks.
    The table has four columns: habit_name, first_inactive_time, last_inactive_time, and inactive streak.
    The habit name column is a string of up to 30 characters long that stores the name of the habit associated with an entry in this table.        The first inactive time column is a date object that stores when an entry was created for this particular instance of an inactive streak (i.e., when it started).
    The last inactive time column is also a date object but it records when the most recent
    
    Parameters
    ----------
        db
            Connect to the database
    """
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS inactive_log (habit_name VARCHAR(30), first_inactive_time DATE, last_inactive_time DATE, inactive_streak INT, inactive_streak_type VARCHAR(10));")
    db.commit()
