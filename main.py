import questionary
import dbsystem
import getter
from habit import Habit
import analytics
import graphics
from style import *

# Welcoming the user by displaying a nice ASCII art
print(f"{CYAN}"+graphics.intro)


def menu():
    """
    This is the command line interface to display the menu and accepts the users input
    """
    # Shows options for the user to choose from
    choice = questionary.select(
        "Please select your choice:",
        choices=[
            'Add a habit',
            'Delete a habit',
            'List all habits',
            'Mark a habit completed',
            'Update a habit',
            'Clear habits',
            'Analytics',
            'Exit'
        ], style=custom_style_fancy
    ).ask()

    # user chooses to add a habit
    if (choice == "Add a habit"):
        habit_name = getter.get_habit_name()
        habit_periodicity = getter.get_habit_periodicity()
        habit_duration = getter.get_habit_duration()
        streak_type = None

        # assign appropriate value to strea_type based on the periodicity
        if (habit_periodicity == 'Daily'):
            streak_type = 'day(s)'
        elif (habit_periodicity == 'Weekly'):
            streak_type = 'week(s)'
        elif (habit_periodicity == 'Monthly'):
            streak_type = 'month(s)'
        else:
            streak_type = 'year(s)'

        # if the user presses ctrl c, abort
        if (habit_name == None or habit_periodicity == None or streak_type == None):
            print(f"\n{RED}Cancelled by user{END}\n")

        # if the user never pressed ctrl c, go on and add the habit
        else:
            # create an object from the Habit class and call the add function
            habit = Habit(habit_name, habit_periodicity,
                          habit_duration, 0, streak_type)
            habit.add()

    # user chooses to delete a habit
    elif (choice == "Delete a habit"):
        db = dbsystem.connect_db()
        habits_only = getter.get_habits_only(db)
        if (habits_only is not None):
            habit_name = questionary.select(
                "Please select the habit to delete:",
                choices=sorted(habits_only), style=custom_style_fancy
            ).ask()
            habit = Habit(habit_name)
            prompt = questionary.text(
                f"Are you sure you want to delete \"{habit.name}\"? Y/N", style=custom_style_fancy).ask()
            if (prompt == "Y" or prompt == "y"):
                habit.delete()
            else:
                print(f"\n{RED}*****{habit} is not deleted!*****{END}\n")

        else:
            print(f"\n{RED}****No Habits in the Database****{END}\n")

    # user chooses to list all habits
    elif (choice == "List all habits"):
        analytics.show_all_habits()

    # user chooses to check off a habit
    elif (choice == "Mark a habit completed"):
        db = dbsystem.connect_db()
        habits_only = getter.get_habits_only(db)
        if (habits_only is not None):
            habit_name = questionary.select(
                "Please select the habit to mark as completed:",
                choices=sorted(habits_only), style=custom_style_fancy
            ).ask()
            habit = Habit(habit_name)
            habit.mark_habit_done()
        else:
            print(f"\n{RED}****No Habits in the Database****{END}\n")

    # user chooses to update a habit
    elif (choice == "Update a habit"):
        db = dbsystem.connect_db()
        habits_only = getter.get_habits_only(db)
        if (habits_only is not None):
            old_name = questionary.select(
                "Please select the habit to update:",
                choices=sorted(habits_only), style=custom_style_fancy
            ).ask()
            new_name = questionary.text(
                "Please type a new name for the selected habit (Just press enter if you want to keep the old name):", style=custom_style_fancy).ask()

            if (new_name == ""):
                new_name = old_name

            new_periodicity = questionary.select("Please select a new periodicity for the selected habit:",
                                                 choices=[
                                                     "Daily",
                                                     "Weekly",
                                                     "Monthly",
                                                     "Yearly"
                                                 ], style=custom_style_fancy).ask()
            new_duration = questionary.text(
                "Please type a new duration for the selected habit:", style=custom_style_fancy).ask()
            cursor = db.cursor()
            habit = Habit(new_name, new_periodicity, new_duration)
            habit.update_habit(old_name)
        else:
            print(f"\n{RED}****No Habits in the Database****{END}\n")

    # user chooses to clear aaa habits
    elif (choice == "Clear habits"):
        choice = questionary.text(
            "Are you sure? Y/N", style=custom_style_fancy).ask()
        if (choice == "Y" or choice == "y"):
            db = dbsystem.connect_db()
            dbsystem.clear_habits(db)
            print(f"\n{GREEN}********All habits have been removed********{END}\n")
        else:
            print(f"\n{RED}********No habits have been removed********{END}\n")

    # user chooses to see the analytics options
    elif (choice == "Analytics"):
        option = questionary.select(
            "Please select your choice:",
            choices=[
                "List habits based on periodicity",
                "List all currently tracked habits",
                "Show the habit(s) with the longest current run streak",
                "Show longest ever streak for a habit",
                "Show all completed dates for a habit",
                "Show inactivity for a habit",
                "Show longest ever inactivity for a habit",
                "Back to main menu"
            ], style=custom_style_fancy
        ).ask()

        if (option == "List habits based on periodicity"):
            sub_option = questionary.select(
                "Please select the periodicity:",
                choices=[
                    "List all daily habits",
                    "List all weekly habits",
                    "List all monthly habits",
                    "List all yearly habits",
                    "Back to main menu"
                ], style=custom_style_fancy
            ).ask()

            if (sub_option == "List all daily habits"):
                analytics.show_daily_habits()

            elif (sub_option == "List all weekly habits"):
                analytics.show_weekly_habits()

            elif (sub_option == "List all monthly habits"):
                analytics.show_monthly_habits()

            elif (sub_option == "List all yearly habits"):
                analytics.show_yearly_habits()

            elif (option == "Back to main menu"):
                menu()

        elif (option == "List all currently tracked habits"):
            analytics.currently_tracked_habits()

        elif (option == "Show the habit(s) with the longest current run streak"):
            sub_option = questionary.select(
                "Please select the periodicity:",
                choices=[
                    "Longest daily habit streak",
                    "Longest weekly habit streak",
                    "Longest monthly habit streak",
                    "Longest yearly habit streak",
                    "Back to main menu"
                ], style=custom_style_fancy
            ).ask()

            if (sub_option == "Longest daily habit streak"):
                analytics.longest_daily_habit_streak()
            elif (sub_option == "Longest weekly habit streak"):
                analytics.longest_weekly_habit_streak()
            elif (sub_option == "Longest monthly habit streak"):
                analytics.longest_monthly_habit_streak()
            elif (sub_option == "Longest yearly habit streak"):
                analytics.longest_yearly_habit_streak()

        elif (option == "Show all completed dates for a habit"):
            analytics.completed_dates()

        elif (option == "Show longest ever streak for a habit"):
            analytics.longest_ever_streak()

        elif (option == "Show inactivity for a habit"):
            analytics.inactivity()

        elif (option == "Show longest ever inactivity for a habit"):
            analytics.longest_ever_inactivity()

        elif (option == "Back to main menu"):
            menu()

    # user chooses to exit the app
    elif (choice == "Exit"):
        print(f"{MAGENTA}" + graphics.outro)
        exit()


if __name__ == "__main__":
    while (True):
        menu()
