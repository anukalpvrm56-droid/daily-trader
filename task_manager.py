"""
task_manager.py
Functions for creating, retrieving, and updating tasks.
A task is represented as a plain dictionary (see the architecture notes),
which keeps it simple to store directly as JSON without any conversion step.
"""

STATUS_OPTIONS = ["Not Started", "In Progress", "Completed"]


def generate_next_id(tasks):
    """Work out the next unique task ID based on the current list."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(tasks, name, category, planned_minutes, date):
    """Create a new task and append it to the tasks list. Returns the new task."""
    new_task = {
        "id": generate_next_id(tasks),
        "date": date,
        "name": name,
        "category": category,
        "planned_minutes": planned_minutes,
        "actual_minutes": 0,
        "status": "Not Started",
    }
    tasks.append(new_task)
    return new_task


def get_tasks_by_date(tasks, date):
    """Return only the tasks scheduled for a specific date."""
    return [task for task in tasks if task["date"] == date]


def find_task_by_id(tasks, task_id):
    """Find a task by its ID. Returns None if no match is found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task_progress(task, actual_minutes=None, status=None):
    """Update a task's actual time and/or status. Modifies the task in place."""
    if actual_minutes is not None:
        task["actual_minutes"] = actual_minutes
    if status is not None:
        task["status"] = status
    return task
