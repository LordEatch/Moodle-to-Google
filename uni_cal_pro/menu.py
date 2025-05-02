from uni_cal_pro import moodle
from uni_cal_pro import utility
from uni_cal_pro import google_calendar

DIVIDER = "-" * 80


def input_moodle_url():
    """
    Prompt the user to enter a Moodle calendar URL, with validation and saved URL fallback.
    """

    url_saved = moodle.is_url_saved()

    print(DIVIDER)

    if url_saved:
        print("A Moodle calendar has been previously saved.")
        print("Leave the line blank to use the saved URL, or enter a new one:")
    else:
        print("No Moodle calendar URL has been saved.")
        print("Please enter the URL for your Moodle calendar:")

    while True:
        moodle_url_input = input("> ").strip()

        if url_saved and moodle_url_input == "":
            print(DIVIDER)
            return moodle.get_saved_url()

        if utility.is_calendar_file(moodle_url_input):
            print("\n✅ The given calendar URL is valid.")
            moodle.save_url(moodle_url_input)
            print(DIVIDER)
            return moodle_url_input

        print("\n❌ That URL did not work. Please enter another:")

def input_moodle_event_filters():
    """
    Ask the user what tags they would like to use to exclusively filter moodle events.
    """

    print(DIVIDER)
    print("Enter any exclusive filters for event summaries.")
    print("Separate filters with commas (e.g., quiz, assignment). Leave blank for no filters.")

    filters_input = input("> ")
    filters = {f.strip() for f in filters_input.split(',') if f.strip()}

    print(DIVIDER)

    return filters

def input_google_calendar_id(service):
    """
    Prompt user for Google Calendar ID, with saved fallback and validation.
    """

    id_saved = google_calendar.is_calendar_id_saved()

    print(DIVIDER)

    if id_saved:
        print("A Google Calendar ID has been previously saved.")
        print("Leave the line blank to use the saved ID, or enter a new one ('primary' for your main calendar):")
    else:
        print("No Google Calendar ID has been saved.")
        print("Please enter the ID for your Google Calendar ('primary' for your main calendar):")

    while True:
        calendar_id_input = input("> ").strip()

        if id_saved and calendar_id_input == "":
            print(DIVIDER)
            return google_calendar.get_saved_calendar_id()

        if google_calendar.calendar_id_exists(service, calendar_id_input):
            print("\n✅ The given calendar ID is valid.")
            google_calendar.save_calendar_id(calendar_id_input)
            print(DIVIDER)
            return calendar_id_input

        print("\n❌ That calendar ID did not work. Please enter another:")

def script_done():
    print(DIVIDER)
    print("Script complete.")
    print(DIVIDER)