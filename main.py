#!/usr/bin/env python3
"""Log daily habits and show streaks."""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DEFAULT_FILE = Path.home() / ".local" / "share" / "habit-tracker" / "habits.json"


def load(path):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error reading {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    return data if isinstance(data, dict) else {}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        print("Error: date must be YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)


def streak(dates, today=None):
    """Current consecutive-day streak ending today (or yesterday)."""
    if not dates:
        return 0
    today = today or date.today()
    day = today if today in dates else today - timedelta(days=1)
    count = 0
    while day in dates:
        count += 1
        day -= timedelta(days=1)
    return count


def longest_streak(dates):
    best = current = 0
    prev = None
    for day in sorted(dates):
        current = current + 1 if prev and day == prev + timedelta(days=1) else 1
        best = max(best, current)
        prev = day
    return best


def main():
    parser = argparse.ArgumentParser(description="Log daily habits and show streaks.")
    parser.add_argument("--file", default=str(DEFAULT_FILE),
                        help="Habits file (default: ~/.local/share/habit-tracker/habits.json)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log a habit for a day")
    p_log.add_argument("habit", help="Habit name, e.g. read")
    p_log.add_argument("--date", default=date.today().isoformat(),
                       help="Date, YYYY-MM-DD (default: today)")

    p_show = sub.add_parser("show", help="Show streaks for all habits")
    p_show.add_argument("habit", nargs="?", default=None,
                        help="Only show this habit")

    p_list = sub.add_parser("list", help="List habits and their logged dates")
    p_list.add_argument("habit", nargs="?", default=None)
    args = parser.parse_args()
    path = Path(args.file).expanduser()
    data = load(path)

    if args.command == "log":
        day = parse_date(args.date)
        dates = {date.fromisoformat(d) for d in data.get(args.habit, [])}
        if day in dates:
            print(f"{args.habit} already logged for {day}.")
            return
        dates.add(day)
        data[args.habit] = sorted(d.isoformat() for d in dates)
        save(path, data)
        print(f"Logged {args.habit} for {day}. "
              f"Current streak: {streak(dates)} day(s).")
    elif args.command == "show":
        habits = [args.habit] if args.habit else sorted(data)
        if not habits:
            print("No habits logged yet. Use: log <habit>")
            return
        for habit in habits:
            dates = {date.fromisoformat(d) for d in data.get(habit, [])}
            print(f"{habit:<20} total: {len(dates):>3}  "
                  f"current streak: {streak(dates)}  "
                  f"longest: {longest_streak(dates)}")
    elif args.command == "list":
        habits = [args.habit] if args.habit else sorted(data)
        if not habits:
            print("No habits logged yet.")
            return
        for habit in habits:
            dates = data.get(habit, [])
            print(f"{habit}: {', '.join(dates) if dates else '(none)'}")


if __name__ == "__main__":
    main()
