"""
main.py
Entry point for the Daily Planning & Progress Tracker.
This file handles the menu and user interaction only - it delegates
actual work to storage.py, task_manager.py, and calculations.py.

Run with:  python main.py
"""

import storage
import task_manager
import calculations
import utils

SUGGESTED_CATEGORIES = ["study", "coding", "exercise", "personal", "work", "other"]


def display_menu():
    print("\n" + "=" * 42)
    print("   DAILY PLANNER & PROGRESS TRACKER")
    print("=" * 42)
    print("1. Add a task")
    print("2. View today's tasks")
    print("3. Update a task")
    print("4. Daily summary")
    print("5. Weekly summary")
    print("6. Exit")
    print("-" * 42)


def display_task(task):
    """Print one task along with its calculated progress."""
    progress = calculations.calculate_task_completion(task)
    print(f"\n[ID {task['id']}] {task['name']}  ({task['category']})")
    print(f"   Status: {task['status']}")
    print(f"   Planned: {progress['planned_minutes']} min | "
          f"Actual: {progress['actual_minutes']} min | "
          f"Remaining: {progress['remaining_minutes']} min")
    print(f"   Completion: {progress['completion_percentage']}%")


def handle_add_task(tasks):
    print("\n--- Add a New Task ---")
    name = utils.get_non_empty_text("Task name: ")
    print(f"Suggested categories: {', '.join(SUGGESTED_CATEGORIES)}")
    category = utils.get_non_empty_text("Category: ").lower()
    planned_minutes = utils.get_positive_int_input("Planned duration (minutes): ")
    date = utils.get_date_input()

    new_task = task_manager.add_task(tasks, name, category, planned_minutes, date)
    storage.save_tasks(tasks)
    print(f"\nTask added successfully! (ID: {new_task['id']})")


def handle_view_today(tasks):
    today = utils.today_str()
    todays_tasks = task_manager.get_tasks_by_date(tasks, today)

    print(f"\n--- Tasks for Today ({today}) ---")
    if not todays_tasks:
        print("No tasks found for today.")
        return
    for task in todays_tasks:
        display_task(task)


def handle_update_task(tasks):
    print("\n--- Update a Task ---")
    if not tasks:
        print("No tasks exist yet. Add one first.")
        return

    task_id = utils.get_positive_int_input("Enter the task ID to update: ")
    task = task_manager.find_task_by_id(tasks, task_id)

    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    display_task(task)
    actual_minutes = utils.get_positive_int_input("Enter actual time completed (minutes): ")
    status = utils.get_choice_input(
        f"Enter status ({'/'.join(task_manager.STATUS_OPTIONS)}): ",
        task_manager.STATUS_OPTIONS,
    )

    task_manager.update_task_progress(task, actual_minutes=actual_minutes, status=status)
    storage.save_tasks(tasks)
    print("\nTask updated successfully!")
    display_task(task)


def handle_daily_summary(tasks):
    date = utils.get_date_input("Enter date for summary (YYYY-MM-DD) or press Enter for today: ")
    stats = calculations.calculate_daily_stats(tasks, date)

    print(f"\n--- Daily Summary for {date} ---")
    if stats["total_tasks"] == 0:
        print("No tasks were planned for this date.")
        return

    print(f"Total tasks: {stats['total_tasks']}")
    print(f"Completed tasks: {stats['completed_tasks']}")
    print(f"Incomplete tasks: {stats['incomplete_tasks']}")
    print(f"Total planned time: {stats['total_planned_minutes']} min")
    print(f"Total actual time: {stats['total_actual_minutes']} min")
    print(f"Overall completion: {stats['overall_completion_percentage']}%")

    # Simple end-of-day message based on how the day went
    percentage = stats["overall_completion_percentage"]
    if percentage >= 90:
        print("\nGreat job! You had an excellent day.")
    elif percentage >= 50:
        print("\nGood effort! Some room to catch up tomorrow.")
    else:
        print("\nTough day - consider adjusting tomorrow's plan.")


def handle_weekly_summary(tasks):
    date_list = utils.date_range_last_n_days(7)
    stats = calculations.calculate_weekly_stats(tasks, date_list)

    print(f"\n--- Weekly Summary ({date_list[0]} to {date_list[-1]}) ---")
    print(f"Tasks planned: {stats['total_tasks_planned']}")
    print(f"Tasks completed: {stats['total_tasks_completed']}")
    print(f"Average daily completion: {stats['average_completion_percentage']}%")
    print(f"Total planned time: {stats['total_planned_minutes']} min")
    print(f"Total actual time: {stats['total_actual_minutes']} min")

    if stats["best_day"]:
        print(f"\nBest day: {stats['best_day']['date']} "
              f"({stats['best_day']['overall_completion_percentage']}%)")
        print(f"Worst day: {stats['worst_day']['date']} "
              f"({stats['worst_day']['overall_completion_percentage']}%)")
    else:
        print("\nNot enough data yet for a best/worst day comparison.")


def main():
    tasks = storage.load_tasks()
    print("Welcome to your Daily Planner!")

    menu_actions = {
        "1": handle_add_task,
        "2": handle_view_today,
        "3": handle_update_task,
        "4": handle_daily_summary,
        "5": handle_weekly_summary,
    }

    while True:
        display_menu()
        choice = utils.get_menu_choice("Choose an option (1-6): ", list(menu_actions.keys()) + ["6"])

        if choice == "6":
            print("\nGoodbye! Your data has been saved.")
            break

        menu_actions[choice](tasks)


if __name__ == "__main__":
    main()
