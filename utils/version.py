# utils/version.py

"""
Version tracking utility for the Transition Generator app.

- Update MANUAL_VERSION when logic changes significantly.
- AUTO_VERSION is updated automatically based on file modification timestamps.
"""

import os
import datetime

# Change this when a significant manual version bump is needed
MANUAL_VERSION = "v1.3.0"

# Add any key files you want to track for auto-version timestamp
FILES_TO_WATCH = [
    "utils/transition_cleaner.py",
    "utils/transition_validator.py",
    "utils/geo_checker.py",
    "prompts/transition_meta.txt",
    "prompts/transition_prompt.txt"
]

def get_auto_version():
    latest_mtime = 0
    for path in FILES_TO_WATCH:
        try:
            mtime = os.path.getmtime(path)
            if mtime > latest_mtime:
                latest_mtime = mtime
        except FileNotFoundError:
            continue

    if latest_mtime:
        dt = datetime.datetime.fromtimestamp(latest_mtime)
        return dt.strftime("%Y%m%d-%H%M")
    return "unknown"

def get_version():
    """
    Returns a combined version string: manual + timestamp
    Example: "v1.3.0 (auto-20250515-1142)"
    """
    return f"{MANUAL_VERSION} (auto-{get_auto_version()})"
