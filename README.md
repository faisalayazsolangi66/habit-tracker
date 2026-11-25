# habit-tracker

Log daily habits and show streaks.

Habits are stored in `~/.local/share/habit-tracker/habits.json` by
default; use `--file` to choose a different location.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py [--file habits.json] log read [--date 2026-11-25]
python3 main.py show [habit]
python3 main.py list [habit]
```

## Example

```bash
python3 main.py --file /tmp/habits.json log read
python3 main.py --file /tmp/habits.json log read --date 2026-11-24
python3 main.py --file /tmp/habits.json show
```

Sample output:

```
Logged read for 2026-11-25. Current streak: 1 day(s).
Logged read for 2026-11-24. Current streak: 2 day(s).
read                 total:   2  current streak: 2  longest: 2
```

## License

MIT — see `LICENSE`.
