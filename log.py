import dbsystem
from style import *

class Log:
    """
    A class used to represent a Log

    ...

    Attributes
    ----------
    habit_name
        Store the name of the habit
    first_completed_time
        Store the time when the habit was first completed
    current_completed_time
        Set the current_completed_time attribute of a habit object
    streak
        Store the number of days that a habit has been completed in a row
    streak_type
        Determine if the streak is a daily, weekly or monthly streak
    db_name
        Specify the name of the database file
        
    Methods
    -------
    add()
        adds an instance of the Log class to the database.
    """
    def __init__(self, habit_name = None, first_completed_time = None, current_completed_time = None, streak = 0, streak_type = None, db_name = "database.db"):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class with all of its attributes.
        
        
        Parameters
        ----------
            self
                Refer to the instance of the class
            habit_name
                Store the name of the habit
            first_completed_time
                Store the time when the habit was first completed
            current_completed_time
                Set the current_completed_time attribute of a habit object
            streak
                Store the number of days that a habit has been completed in a row
            streak_type
                Determine if the streak is a daily, weekly or monthly streak
            db_name
                Specify the name of the database file
        
        Returns
        -------
        
            The object itself
        """
        self.habit_name = habit_name
        self.first_completed_time = first_completed_time
        self.current_completed_time = current_completed_time
        self.streak = streak
        self.streak_type = streak_type
        self.db = dbsystem.connect_db(db_name)
        
    def add(self):
        """
        The add function adds a new habit to the database.
            Args:
                self (object): The object that is being added to the database.
        
        Parameters
        ----------
            self
                Refer to the instance of the class
        """
        cursor = self.db.cursor()
        cursor.execute(f"INSERT INTO log VALUES ('{self.habit_name}', '{self.first_completed_time}', '{self.current_completed_time}','{self.streak}', '{self.streak_type}')")
        self.db.commit()

class InactiveLog:
    """
     A class used to represent InactiveLog

     ...

    Attributes
    ----------
    habit_name
        Set the name of the habit
    last_inactive_time
        Store the last time a habit was inactive
    first_inactive_time
        Set the first time that a habit was inactive
    inactive_streak
        Keep track of how long the user has been inactive
    inactive_streak_type
        Determine the type of streak
    db_name
        Specify the name of the database file
        
    Methods
    -------
    add()
        adds an instance of the InactiveLog class to the database.
    """
    def __init__(self, habit_name = None, last_inactive_time = None, first_inactive_time = None, inactive_streak = 0, inactive_streak_type = None, db_name = "database.db"):
        """
        The __init__ function is called when an object of the class is created.
        It initializes all the attributes of the class, and sets them to their default values.
        
        Parameters
        ----------
            self
                Refer to the object itself
            habit_name
                Set the name of the habit
            last_inactive_time
                Store the last time a habit was inactive
            first_inactive_time
                Set the first time that a habit was inactive
            inactive_streak
                Keep track of how long the user has been inactive
            inactive_streak_type
                Determine the type of streak
            db_name
                Specify the name of the database file
        """
        self.habit_name = habit_name
        self.last_inactive_time = last_inactive_time
        self.first_inactive_time = first_inactive_time
        self.streak = inactive_streak
        self.streak_type = inactive_streak_type
        self.db = dbsystem.connect_db(db_name)

    def add(self):
        """
        The add function adds a new inactive_log to the database.
            Args:
                self (dbsystem): The dbsystem object that is calling this function.
                habit_name (str): The name of the habit that has been logged as inactive. 
                last_inactive_time (datetime): The time at which the user was last marked as inactive for this particular habit. 
        
        Parameters
        ----------
            self
                Access the attributes and methods of the class
        """
        cursor = self.db.cursor()
        cursor.execute(f"INSERT INTO inactive_log VALUES ('{self.habit_name}', '{self.last_inactive_time}', '{self.first_inactive_time}', '{self.streak}', '{self.streak_type}')")
        self.db.commit()