"""
calculations.py
All the "number crunching" for the planner: per-task completion,
daily statistics, and weekly statistics. Kept separate from task_manager
so that task storage/editing and progress math don't get tangled together.
"""

from task_manager import get_tasks_by_date


def calculate_task_completion(task):
    """Return planned/actual/remaining time and completion percentage for one task."""
    planned = task["planned_minutes"]
    actual = task["actual_minutes"]

    # Completion percentage is capped at 100 - going over planned time still counts as "done"
    percentage = 0 if planned == 0 else min(100.0, round((actual / planned) * 100, 1))
    remaining = max(0, planned - actual)

    return {
        "planned_minutes": planned,
        "actual_minutes": actual,
        "remaining_minutes": remaining,
        "completion_percentage": percentage,
    }


def calculate_daily_stats(tasks, date):
    """Calculate summary statistics across all tasks for a single date."""
    day_tasks = get_tasks_by_date(tasks, date)

    total_tasks = len(day_tasks)
    completed_tasks = sum(1 for task in day_tasks if task["status"] == "Completed")
    incomplete_tasks = total_tasks - completed_tasks

    total_planned = sum(task["planned_minutes"] for task in day_tasks)
    total_actual = sum(task["actual_minutes"] for task in day_tasks)

    overall_percentage = 0 if total_planned == 0 else round(min(100.0, (total_actual / total_planned) * 100), 1)

    return {
        "date": date,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "incomplete_tasks": incomplete_tasks,
        "total_planned_minutes": total_planned,
        "total_actual_minutes": total_actual,
        "overall_completion_percentage": overall_percentage,
    }


def calculate_weekly_stats(tasks, date_list):
    """Calculate a summary across a list of dates (normally the last 7 days).
    'Best' and 'worst' day are based on overall completion percentage,
    and only consider days that actually had tasks planned."""
    daily_breakdown = [calculate_daily_stats(tasks, date) for date in date_list]
    days_with_tasks = [day for day in daily_breakdown if day["total_tasks"] > 0]

    total_tasks_planned = sum(day["total_tasks"] for day in daily_breakdown)
    total_tasks_completed = sum(day["completed_tasks"] for day in daily_breakdown)
    total_planned_minutes = sum(day["total_planned_minutes"] for day in daily_breakdown)
    total_actual_minutes = sum(day["total_actual_minutes"] for day in daily_breakdown)

    if days_with_tasks:
        average_completion = round(
            sum(day["overall_completion_percentage"] for day in days_with_tasks) / len(days_with_tasks), 1
        )
        best_day = max(days_with_tasks, key=lambda day: day["overall_completion_percentage"])
        worst_day = min(days_with_tasks, key=lambda day: day["overall_completion_percentage"])
    else:
        average_completion = 0
        best_day = None
        worst_day = None

    return {
        "date_range": date_list,
        "total_tasks_planned": total_tasks_planned,
        "total_tasks_completed": total_tasks_completed,
        "average_completion_percentage": average_completion,
        "total_planned_minutes": total_planned_minutes,
        "total_actual_minutes": total_actual_minutes,
        "best_day": best_day,
        "worst_day": worst_day,
        "daily_breakdown": daily_breakdown,
    }
