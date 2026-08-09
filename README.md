# Daily Planner & Progress Tracker (Prototype)

A command-line tool for planning your day and tracking how much you actually got done.

## How to run

1. Make sure Python 3 is installed.
2. Open a terminal in this folder.
3. Run:

   ```
   python main.py
   ```

4. A file called `tasks_data.json` will be created automatically in this folder
   the first time you add a task. This is where your data is stored between runs.

## Files

| File               | Purpose                                              |
|--------------------|-------------------------------------------------------|
| `main.py`          | Menu loop and user interaction                        |
| `storage.py`        | Reads/writes `tasks_data.json`                        |
| `task_manager.py`   | Creating, finding, and updating tasks                 |
| `calculations.py`   | Progress math: per-task, daily, and weekly statistics |
| `utils.py`           | Input validation and date helpers                     |
| `tasks_data.json`   | Your saved data (created automatically, not included) |

## Notes

- "Weekly summary" looks at the rolling last 7 days (today and the 6 days before it),
  not a fixed Monday–Sunday calendar week.
- Completion percentage per task/day is capped at 100% even if actual time exceeds planned time.
