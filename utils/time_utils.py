# utils/time_utils.py

import datetime

def seconds_to_hms(seconds):
    """Convert seconds to HH:MM:SS string."""
    return str(datetime.timedelta(seconds=seconds))

def now_str():
    """Return current timestamp as string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# utils/time_utils.py for OptiTradeBot

import time
from datetime import datetime

def format_seconds(seconds):
    """Convert seconds to a human-readable format (e.g., '2m 30s')."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    mins, secs = divmod(seconds, 60)
    if mins < 60:
        return f"{mins}m {secs}s"
    hours, mins = divmod(mins, 60)
    return f"{hours}h {mins}m {secs}s"

def now_str():
    """Return current time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_time(timestr):
    """Parse a time string into a datetime object."""
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

def seconds_since(timestr):
    """Return seconds since a given time string."""
    dt = parse_time(timestr)
    return int((datetime.now() - dt).total_seconds())

def sleep_until(target_time):
    """Sleep until the specified datetime (as string or datetime object)."""
    if isinstance(target_time, str):
        target_time = parse_time(target_time)
    now = datetime.now()
    delta = (target_time - now).total_seconds()
    if delta > 0:
        time.sleep(delta)
