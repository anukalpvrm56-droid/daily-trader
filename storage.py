"""
storage.py
Handles all reading and writing of task data to a local JSON file.
This is the ONLY module that should know about the file on disk -
every other module just works with a plain Python list of task dicts.
"""

import json
import os

# Store the data file next to this script, regardless of where the program is run from
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks_data.json")


def load_tasks():
    """Load the list of tasks from the JSON file.
    Returns an empty list if the file doesn't exist yet or is unreadable."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: The data file could not be read. Starting with an empty task list.")
        return []


def save_tasks(tasks):
    """Save the current list of tasks to the JSON file. Returns True on success."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
        return True
    except OSError as error:
        print(f"Error: Could not save data ({error}).")
        return False
