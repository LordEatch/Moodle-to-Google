import ics
import os
from uni_cal_pro import config


MOODLE_URL_FILENAME = "moodle_url.txt"
MOODLE_FILENAME = "moodle_calendar.ics"


# Properties.
moodle_url_filepath = os.path.join(config.TEMP_DIRECTORY_PATH, MOODLE_URL_FILENAME)
moodle_filepath = os.path.join(config.TEMP_DIRECTORY_PATH, MOODLE_FILENAME)


def filter_events(events, unwanted_summary_substrings):
    """Take a set of ics events. Return a new list with events whose name does not contain any of the strings from unwanted_summary_substrings."""

    unwanted_events = {
        e for e in events
        for substring in unwanted_summary_substrings
        if substring in e.name.lower()
        }

    return events.difference(unwanted_events)

def filter_calendar(calendar_path, unwanted_summary_substrings):
    # Instantiate a calendar object by reading the calendar file's contents.
    with open(calendar_path) as calendar_txt:
        calendar = ics.Calendar(calendar_txt.read())

    filtered_events = filter_events(set(calendar.events), unwanted_summary_substrings)

    return filtered_events

def save_url(url):
    with open(moodle_url_filepath, "w") as file:
        file.write(url)

    print("\tUrl saved for later use.")

def is_url_saved():
    return os.path.exists(moodle_url_filepath)

def get_saved_url():
    if is_url_saved:
        with open(moodle_url_filepath) as file:
            return file.read()
    else:
        raise FileNotFoundError(f"The file {moodle_url_filepath} does not exist.")