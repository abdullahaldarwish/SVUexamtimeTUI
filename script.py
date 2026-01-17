import curses
import time
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os
import argparse

parser = argparse.ArgumentParser(description="Exam Countdown TUI")
parser.add_argument("--interval", "-i", type=str, default="5m", help="Refresh interval (e.g., 5m for 5 minutes)")
args = parser.parse_args()

def parse_duration(duration_str):
    """
    Convert a duration string like '1m', '5m', '2h', '1d' into seconds.
    """
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        unit = duration_str[-1]
        value = int(duration_str[:-1])
        final = value * units[unit]
        if final >59:
            return final
        else:
            raise ValueError("Duration must be at least 60 seconds.")
    except (Exception):
        raise ValueError("Invalid duration. Use e.g., 1m, 5m, 2h, 1d.")

HTML_FILE = "exams.html"
REFRESH_SECONDS = parse_duration(args.interval)

if not (os.path.exists(HTML_FILE) and os.path.getsize(HTML_FILE) > 0):
    print("enter table HTML data, end with Ctrl-D (Ctrl-Z + Enter on Windows):")

    tableHTML = sys.stdin.read()

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(tableHTML)

def load_exams_from_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    table = soup.find("table", id="results")
    rows = table.find_all("tr")[2:]

    exams = []

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 8:
            continue

        course = cols[1]
        date_str = cols[3]
        start_time = cols[4]

        exam_dt = datetime.strptime(
            f"{date_str} {start_time}", "%Y-%m-%d %H:%M:%S"
        )

        exams.append({
            "course": course,
            "datetime": exam_dt
        })

    return exams


def format_remaining(delta):
    if delta.total_seconds() <= 0:
        return "YOU PASSED IT, RIGHT?"

    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes = rem // 60

    return f"{days}d {hours}h {minutes}m"


def tui(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, curses.COLOR_RED, -1)
    curses.init_pair(5, curses.COLOR_GREEN, -1)

    last_load = None
    exams = []

    while True:
        now = datetime.now()
        if not last_load or (now - last_load).seconds >= REFRESH_SECONDS:
            exams = load_exams_from_html()
            last_load = now

        stdscr.clear()
        stdscr.addstr(0, 0, "Exam Countdown TUI", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))

        row = 3
        for exam in exams:
            remaining = exam["datetime"] - now
            remaining_str = format_remaining(remaining)

            if remaining.total_seconds() < 86400:
                color = curses.color_pair(4) | curses.A_BOLD
            else:
                color = curses.color_pair(3)

            line = (
                f"{exam['course']:<8} | "
                f"{exam['datetime'].strftime('%Y-%m-%d %H:%M')} | "
                f"{remaining_str}"
            )

            stdscr.addstr(row, 0, line, color)
            row += 1

        stdscr.addstr(
            row + 1,
            0,
            f"Last reload: {last_load.strftime('%H:%M:%S')} | "
            f"Reloading every {args.interval} | Ctrl+C to exit",
            curses.color_pair(5)
        )

        stdscr.refresh()
        time.sleep(REFRESH_SECONDS // 5)


if __name__ == "__main__":
    curses.wrapper(tui)
