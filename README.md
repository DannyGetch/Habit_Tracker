<!-- TABLE OF CONTENTS -->

# Table of Contents

- [Habit Tracker](#habit-tracker)
  - [Habit Tracker's Core Functionality](#habit-tracker-s-core-functionality)
    - [Progress and Streak Tracker](#progress-and-streak-tracker)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Installing](#installing)
    - [Packages for running tests](#packages-for-running-tests)
  - [How To Run the Program](#how-to-run-the-program)
  - [Running Tests](#running-tests)
- [Usage](#usage)
  - [Add a habit](#add-a-habit)
  - [Delete a habit](#delete-a-habit)
  - [List all habits](#list-all-habits)
  - [Mark a habit completed](#mark-a-habit-completed)
  - [Update a habit](#update-a-habit)
  - [Clear habits](#clear-habits)
  - [Analytics](#analytics)
    - [List habits based on periodicity](#list-habits-based-on-periodicity)
    - [List all currently tracked habits](#list-all-currently-tracked-habits)
    - [Show the habit(s) with the longest current run streak](<#show-the-habit(s)-with-the-longest-current-run-streak>)
    - [Show longest ever streak for a habit](#show-longest-ever-streak-for-a-habit)
    - [Show all completed dates for a habit](#show-all-completed-dates-for-a-habit)
    - [Show inactivity for a habit](#show-inactivity-for-a-habit)
    - [Show longest ever inactivity for a habit](#show-longest-ever-inactivity-for-a-habit)
    - [Back to main menu](#back-to-main-menu)
  - [Exit](#exit)
- [Contributing](#contributing)
- [Contact](#contact)

# Habit Tracker

Good habits are behaviors that we develop over time and can have a positive impact on our lives. Good habits can help us achieve our goals and improve our lives. There are many strategies for developing good habits, and one is using an app.

With this habit tracker, you can easily track your daily, weekly, monthly, or yearly habits and monitor your progress over time. This app offers a simple and attractive interface that allows you to check off your habits as you complete them. It also has an analytics section where you can see details of your missed dates. The program is a part of _IU University's_ _DLBDSOOFPP01_ course and uses Python 3.9 as the backend of the program.

## Habit Tracker's Core Functionality

The habit tracker essentially allows a user to:

- Add a habit
- Delete a habit
- List all habits
- Mark a habit completed
- Update a habit
- Clear habits

### Progress and Streak Tracker

Additionally, the user can view the following analytics:

- List habits based on periodicity
- List all currently tracked habits
- Show the habit(s) with the longest current run streak
- Show longest ever streak for a habit
- Show all completed dates for a habit
- Show inactivity for a habit
- Show longest ever inactivity for a habit

# Getting Started

**Important**: Make sure that Python 3.8 + is installed on your OS. You can download the latest version of Python from [this link.](https://www.python.org/downloads/)

## Dependencies

- Python 3.8 +
- Questionary 1.10.0 +
- Tabulate 0.9.0

## Installing

You can download the latest version of Python from [this link.](https://www.python.org/downloads/) - Make sure to check "ADD to path" in the Python installer. <br>

<br> After installing Python, you can proceed and install the following libraries. <br>

<br>[Questionary](https://pypi.org/project/questionary/) - Questionary is a Python library for building pretty command line interfaces.
<br>Install by running the below command:<br>

```
pip3 install questionary
```

<br>[Tabulate](https://pypi.org/project/tabulate/) - Pretty-print tabular data in Python, a library and a command-line utility.
<br>Install by running the below command:<br>

```
pip3 install tabulate
```

If you don't feel like downloading the libraries one by one, you can run the following command to install all the dependancies at once:

```
pip3 install -r requirements.txt
```

### Packages for running tests

To run the tests, you will need the following packages installed:
<br>Pytest - For testing functions:<br>

```
pip3 install -U pytest
```

<br>Freezegun - For freezing time: <br>

```
pip3 install freezegun
```

<br>When you run the test file, make sure to use the -s flag to see console messages:

```
python3 -m pytest -s test.py
```

## How To Run the Program

After installing the dependencies, download the files from this repository (if not downloaded already) and store them in a separate folder. Open your command/terminal window and [cd](https://www.alphr.com/change-directory-in-cmd/) to your downloaded folder. After that, type the following command to execute the program:

```
python3 main.py
```

Doing so will launch the CLI and then you'll be able to see and choose from the following options in your Habit Tracker:

```

██   ██  █████  ██████  ██ ████████     ████████ ██████   █████   ██████ ██   ██ ███████ ██████
██   ██ ██   ██ ██   ██ ██    ██           ██    ██   ██ ██   ██ ██      ██  ██  ██      ██   ██
███████ ███████ ██████  ██    ██           ██    ██████  ███████ ██      █████   █████   ██████
██   ██ ██   ██ ██   ██ ██    ██           ██    ██   ██ ██   ██ ██      ██  ██  ██      ██   ██
██   ██ ██   ██ ██████  ██    ██           ██    ██   ██ ██   ██  ██████ ██   ██ ███████ ██   ██

? Please select your choice: (Use arrow keys)
 » Add a habit
   Delete a habit
   List all habits
   Mark a habit completed
   Update a habit
   Clear habits
   Analytics
   Exit
```

## Running tests

To run the test; navigate to the test folder (included with the repository) through command/terminal by using [cd](https://www.alphr.com/change-directory-in-cmd/) and then type `pytest`.

# Usage

**Important**: You can choose to keep or remove the **main.db** file as it contains the following pre-defined habits: Drink 10 glasses of water, Play football, Go for a swim, Vacation to Germany, and Eat fruits. <br>

## Add a habit

Your first action should start by creating a habit and you can do so by launching the program and selecting:

```
» Add a habit
```

You will then be prompted to enter the name of the habit:

```
? Please Enter the Name of Your Habit:
```

If you provide a name that already exists in the database, the program will show a message and prompt you to enter name again:

```
****Eat fruits already exists. Please enter a different habit.****

? Please Enter the Name of Your Habit:
```

## Delete a habit

This option will show you a list of habits that you have created, you'll have to simply choose the habit you want to delete and press enter. A message will show to confirm your decision. Press Y for yes or any
other key for no.

## List all habits

Lists all the created habits along with their information like _Name, Periodicity, Duration, Streak and Last Completed Date_.

## Mark a habit completed

The user can use this option to mark their habit as completed. <br> Note: A habit can be marked as completed only once during the defined period. <br>
<br>Note: If the user failed to complete their habit within the specified periodicity; then marking the habit as completed will the reset the streak to 1. <br>

## Update a habit

This option allows you to edit the details of a habit including its name. You can not modify the _Streak, Last Completed, and Date Created._

## Clear habits

This removes all habits and clears out the database.

## Analytics

The user can use this option to view different analytics.

```
? Please select your choice: Analytics
? Please select your choice: (Use arrow keys)
 » List habits based on periodicity
   List all currently tracked habits
   Show the habit(s) with the longest current run streak
   Show longest ever streak for a habit
   Show all completed dates for a habit
   Show inactivity for a habit
   Show longest ever inactivity for a habit
   Back to main menu
```

### List habits based on periodicity

This option lists habits based on their periodicity:

```
? Please select the periodicity: (Use arrow keys)
 » List all daily habits
   List all weekly habits
   List all monthly habits
   List all yearly habits
   Back to main menu
```

### List all currently tracked habits

This option lists habits that have a streak greater than 1.

### Show longest ever streak for a habit

This option allows you to choose a habit and see the longest ever streak for it.

### Show all completed dates for a habit

This option allows you to choose a habit and see all the dates that you've marked as completed.

### Show inactivity for a habit

This option allows you to choose a habit and see all the dates that you've missed.

### Show longest ever inactivity for a habit

This option allows you to choose a habit and see the longest ever inactive streak for it.

### Back to main menu

This option takes you back to the main menu.

## Exit

Exits the program.

# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# Contact

Daniel Mekonnen - [Email](mailto:dannygetch@gmail.com)

Project Link: [https://github.com/DannyGetch/Habit_Tracker](https://github.com/DannyGetch/Habit_Tracker)
