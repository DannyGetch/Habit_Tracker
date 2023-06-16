import datetime
import dbsystem

class Habit:
    """
    A class used to represent a Habit

    ...

    Attributes
    ----------
    name
        name of the habit
    periodicity
        periodicity of the habit
    duration
        duration of the habit
    streak
        streak of the habit (default 0)
    streak_type
        streak type of the habit (default None)
    date_last_completed
        last cmpleted date of the habit (default None)
    db_name
        name of the database (default database.db)

    Methods
    -------
    add()
        adds an instance of the Habit class to the database by passing it to the add_habit method in the dbsystem module
    delete()
        deletes an instance of the Habit class from the database by passing its name to the delete_habit method in the dbsystem module
    mark_habit_done()
        checks off a habit by passing its name to the mark_habit_done method in the dbsystem module
    update_habit()
        updates a habit by passing its name to the update_habit method in the dbsystem module
    """
    
    def __init__(self, name = None, periodicity = None, duration = None, streak = 0, streak_type = None, date_last_completed = None, db_name = "database.db"):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its attributes.
        
        
        Parameters
        ----------
            self
                Refer to the instance of the class
            name
                Set the name of the habit
            periodicity
                Determine how often the task should be completed
            duration
                Set the duration of a task
            streak
                Store the current streak of the habit
            streak_type
                Determine the streak type
            date_last_completed
                Set the date_last_completed attribute of the object
            db_name
                Name of the database to connect to
        
        Returns
        -------
        
            The object itself
        """
        self.name = name
        self.periodicity = periodicity
        self.duration = duration
        self.streak = streak
        self.streak_type = streak_type
        self.date_last_comleted = date_last_completed
        self.db = dbsystem.connect_db(db_name)
        self.current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def add(self):
        """
        adds an instance of the Habit class to the database by passing it to the add_habit method in the dbsystem module
        """
        dbsystem.add_habit(self.db, self.name, self.periodicity, self.duration, self.streak, self.streak_type, self.date_last_comleted, self.current_time)
    
    def delete(self):
        """
        deletes an instance of the Habit class from the database by passing its name to the delete_habit method in the dbsystem module
        """
        dbsystem.delete_habit(self.db, self.name)
    
    def mark_habit_done(self):
        """
        checks off a habit by passing its name to the mark_habit_done method in the dbsystem module
        """
        dbsystem.mark_habit_done(self.db, self.name)
    
    def update_habit(self):
        """
        updates a habit by passing its name to the update_habit method in the dbsystem module
        """
        dbsystem.update_habit(self.db, self.name)