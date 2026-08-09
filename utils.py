"""
utils.py
Small helper functions used across the program: input validation,
date handling, and menu prompts. Keeping these separate avoids
repeating the same "keep asking until the input is valid" pattern
everywhere else in the code.
"""

from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


def today_str():
    """Return today's date as a string, e.g. '2026-08-09'."""
    return datetime.now().strftime(DATE_FORMAT)


def is_valid_date(date_text):
    """Check whether a string matches the YYYY-MM-DD format."""
    try:
        datetime.strptime(date_text, DATE_FORMAT)
        return True
    except ValueError:
        return False


def get_date_input(prompt="Enter date (YYYY-MM-DD) or press Enter for today: "):
    """Ask the user for a date. An empty entry defaults to today."""
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return today_str()
        if is_valid_date(user_input):
            return user_input
        print("Invalid date format. Please use YYYY-MM-DD, e.g. 2026-08-09.")


def get_positive_int_input(prompt):
    """Ask the user for a whole number that is zero or greater (e.g. minutes, IDs)."""
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
            if value < 0:
                print("Please enter a number that is zero or greater.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a whole number, e.g. 30.")


def get_non_empty_text(prompt):
    """Ask the user for text that cannot be left blank."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("This field cannot be empty. Please try again.")


def get_choice_input(prompt, valid_choices):
    """Ask the user to pick one option from a fixed list (case-insensitive)."""
    valid_lower = [choice.lower() for choice in valid_choices]
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in valid_lower:
            matched_index = valid_lower.index(user_input.lower())
            return valid_choices[matched_index]  # return with original casing
        print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")


def get_menu_choice(prompt, valid_options):
    """Ask the user to pick a menu option (validated against a list of allowed strings)."""
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            return user_input
        print("Invalid option. Please enter one of:", ", ".join(valid_options))


def date_range_last_n_days(n=7, end_date=None):
    """Return a list of the last n date strings, ending at end_date (default: today), oldest first."""
    end = datetime.now() if end_date is None else datetime.strptime(end_date, DATE_FORMAT)
    return [(end - timedelta(days=offset)).strftime(DATE_FORMAT) for offset in range(n - 1, -1, -1)]
