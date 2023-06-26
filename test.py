import os
import pytest
from freezegun import freeze_time
from habit import Habit
import dbsystem
import getter


@freeze_time("01/01/2015 12:40")
@pytest.fixture
def my_db():
    # Returns a database connection of the test database
    return dbsystem.connect_db(database_name="test_db.db")


@freeze_time("01/01/2016 12:41")
@pytest.fixture
def my_daily_habit():
    # Creates a daily habit for testing
    return Habit("Football", "Daily", "90 days", db_name="test_db.db")


@freeze_time("01/02/2023 12:42")
@pytest.fixture
def my_weekly_habit():
    # Creates a weekly habit for testing
    return Habit("Swim", "Weekly", "20 weeks", db_name="test_db.db")


@freeze_time("01/02/2023 12:42")
@pytest.fixture
def my_monthly_habit():
    # Creates a monthly habit for testing
    return Habit("Play bowling", "Monthly", "20 months", db_name="test_db.db")


@freeze_time("01/02/2017 12:42")
@pytest.fixture
def my_yearly_habit():
    # Creates a yearly habit for testing
    return Habit("Vacation", "Yearly", "100 years", db_name="test_db.db")


def test_add(my_db, my_daily_habit, my_weekly_habit, my_monthly_habit, my_yearly_habit):
    # Adds the created habit to the database
    with freeze_time("01/01/2023 12:49"):
        print("Adding a daily habit to the database")
        my_daily_habit.add()
        assert getter.habit_exists(my_db, my_daily_habit.name)
    with freeze_time("01/02/2023 12:49"):
        print("Adding a weekly habit to the database")
        my_weekly_habit.add()
        assert getter.habit_exists(my_db, my_weekly_habit.name)
    with freeze_time("01/02/2023 12:49"):
        print("Adding a monthly habit to the database")
        my_monthly_habit.add()
        assert getter.habit_exists(my_db, my_monthly_habit.name)
    with freeze_time("01/02/2017 12:49"):
        print("Adding a yearly habit to the database")
        my_yearly_habit.add()
        assert getter.habit_exists(my_db, my_yearly_habit.name)


def test_check_off(my_daily_habit, my_weekly_habit, my_monthly_habit, my_yearly_habit):
    # Checks off the habit first time
    with freeze_time("01/02/2023 13:49"):
        print("Marking a habit completed first day")
        my_daily_habit.mark_habit_done()
    with freeze_time("01/02/2023 13:49"):
        print("Marking a habit completed first week")
        my_weekly_habit.mark_habit_done()
    with freeze_time("01/12/2023 13:49"):
        print("Marking a habit completed first month")
        my_monthly_habit.mark_habit_done()
    with freeze_time("01/12/2017 13:49"):
        print("Marking a habit completed first year")
        my_yearly_habit.mark_habit_done()


def test_check_off_second(my_daily_habit, my_weekly_habit, my_monthly_habit, my_yearly_habit):
    # Checks off the habit second time the same day
    with freeze_time("01/02/2023 14:34"):
        print("Marking a habit completed second time same day")
        my_daily_habit.mark_habit_done()
    # Checks off the habit second time the same week
    with freeze_time("01/02/2023 14:34"):
        print("Marking a habit completed second time same week")
        my_weekly_habit.mark_habit_done()
    # Checks off the habit second time the same month
    with freeze_time("01/14/2023 14:34"):
        print("Marking a habit completed second time same month")
        my_monthly_habit.mark_habit_done()
    # Checks off the habit second time the same year
    with freeze_time("01/14/2017 14:34"):
        print("Marking a habit completed second time same year")
        my_yearly_habit.mark_habit_done()


def test_check_off_third(my_daily_habit, my_weekly_habit, my_monthly_habit, my_yearly_habit):
    # Checks off the habit next day
    with freeze_time("01/03/2023 15:49"):
        print("Marking a habit completed next day")
        my_daily_habit.mark_habit_done()
    # Checks off the habit next weeek
    with freeze_time("01/09/2023 15:49"):
        print("Marking a habit completed next week")
        my_weekly_habit.mark_habit_done()
    # Checks off the habit next month
    with freeze_time("02/09/2023 15:49"):
        print("Marking a habit completed next month")
        my_monthly_habit.mark_habit_done()
    # Checks off the habit next year
    with freeze_time("02/09/2018 15:49"):
        print("Marking a habit completed next year")
        my_yearly_habit.mark_habit_done()


def test_check_off_third(my_daily_habit, my_weekly_habit, my_monthly_habit, my_yearly_habit):
    # Checks off the habit more than a day later
    with freeze_time("01/10/2023 12:49"):
        print("Marking a habit completed more than a day later")
        my_daily_habit.mark_habit_done()
    # Checks off the habit more than a week later
    with freeze_time("01/29/2023 12:49"):
        print("Marking a habit completed more than a week later")
        my_weekly_habit.mark_habit_done()
    # Checks off the habit more than a month later
    with freeze_time("03/29/2023 12:49"):
        print("Marking a habit completed more than a month later")
        my_monthly_habit.mark_habit_done()
    # Checks off the habit more than a year later
    with freeze_time("03/29/2023 12:49"):
        print("Marking a habit completed more than a year later")
        my_yearly_habit.mark_habit_done()


@pytest.fixture
def new_habit():
    # Updates the created habits
    print("Updating a daily habit")
    new_habit = Habit("Bike", "Weekly", "1 year")
    new_habit.update_habit("Football")
    print("Updating a weekly habit")
    new_habit.update_habit("Swim")
    print("Updating a monthly habit")
    new_habit.update_habit("Play bowling")
    print("Updating a yearly habit")
    new_habit.update_habit("Vacation")
    return new_habit


def test_delete(my_db, new_habit):
    # Deletes the updated habit

    print("Deleting habit")
    new_habit.delete()
    assert getter.habit_exists(my_db, new_habit.name) == False


def test_clear(my_db):
    # Clears the data

    print("Clearing all data")
    dbsystem.clear_habits(my_db)


def test_remove_testdb():
    # Removes the test database

    print("Deleting the test database")
    os.remove("test_db.db")
