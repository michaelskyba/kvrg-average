#!/usr/bin/python

import os
import sys
import subprocess

try:
    # Change the next line if your config folder is not $HOME/.config
    config_directory = f"{os.environ['HOME']}/.config"

    # If $HOME isn't set, os.environ['HOME'] will cause an error

except KeyError:
    print("The environment variable $HOME is not set.")
    print("You need to change the config_directory variable.")
    print("See README.md on github (https://github.com/michaelskyba/kvrg-avg) for more information.")

    sys.exit(1)

# If config_directory doesn't exist, print an error an exit
if not os.path.isdir(config_directory):
    print(f"The config directory that is set ({config_directory}) does not exist.")
    print("You need to change the config_directory variable.")
    print("See README.md on github (https://github.com/michaelskyba/kvrg-avg) for more information.")

    sys.exit(1)

# If config_director/avg/trackers does not exist, create it
# mkdir without -p will raise an error if config_directory/avg doesn't exist first
if not os.path.isdir("f{config_directory}/avg/trackers"):
    subprocess.run(["mkdir", "-p", f"{config_directory}/avg/trackers"])

# Starts checking for command-line arguments

# You ran "avg" without any extra arguments, or you ran "avg list"
# running something like "avg list foo bar" is the same
if len(sys.argv) == 1 or sys.argv[1] == "list":

    # Get the tracker names by looking in config/avg/trackers
    tracker_names = os.listdir(f"{config_directory}/avg/trackers")

    # Alert the user if they have no trackers
    if not tracker_names:
        print("You have no trackers.")
        print("Use 'avg create \"<name>\" [\"<description>\"]' to create one.")
        sys.exit(1)

    # Print the tracker names and their average values, if the user has a tracker
    else:
        for tracker in tracker_names:
            with open(f"{config_directory}/avg/trackers/{tracker}", "r") as tracker_file:
                print(f"{tracker} - {tracker_file.readlines()[1].strip()}")
        sys.exit(0)

# You ran "avg create ..."
if sys.argv[1] == "create":
    # If user runs "avg create"
    if len(sys.argv) == 2:
        print("You need a <name> argument.")
        sys.exit(1)

    # Check if config/avg/trackers contains a tracker called <name>
    if sys.argv[2] in os.listdir(f"{config_directory}/avg/trackers"):
        print(f"Tracker with name '{sys.argv[2]}' already exists.")
        sys.exit(1)

    # Create a file with name <name> in config/avg/trackers
    with open(f"{config_directory}/avg/trackers/{sys.argv[2]}", "w") as tracker_file:

        # Saves the description if the user provided one

        # the description is the fourth argument, so the length has to be > 3 (>=4)
        # and sys.argv[3] will get the fourth argument (3rd when not including "avg")
        if len(sys.argv) > 3:
            description = sys.argv[3]
        else:
            description = "(No description)"

        tracker_file.write(f"{description}\n0\n")

    sys.exit(0)

# You ran "avg delete ..."
if sys.argv[1] == "delete":
    # If user runs "avg delete"
    if len(sys.argv) == 2:
        print("You need a <name> argument.")
        sys.exit(1)

    # Removes the tracker file
    try:
        os.remove(f"{config_directory}/avg/trackers/{sys.argv[2]}")

    # Tracker does not exist
    except FileNotFoundError:
        print(f"There is no such tracker '{sys.argv[2]}'.")
        sys.exit(1)

    sys.exit(0)

# You ran "avg push ..."
if sys.argv[1] == "push":
    # If user runs "avg push"
    if len(sys.argv) == 2:
        print("You need a <name> and a <one or more values> argument.")
        sys.exit(1)

    # If user runs "avg push <name>"
    if len(sys.argv) == 3:
        print("You need a <one or more values> argument.")
        sys.exit(1)

    sys.exit(0)

# Invalid command
print(f"'{sys.argv[1]}' is not a kvrg-avg command. See the README for a list of valid commands.")
sys.exit(1)

