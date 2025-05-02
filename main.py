import os
from uni_cal_pro import config
from uni_cal_pro import google_calendar
from uni_cal_pro import menu
from uni_cal_pro import moodle
from uni_cal_pro import utility


def main():
    config.install_missing_packages()

    # Create the local temporary folder.
    os.makedirs(config.TEMP_DIRECTORY_PATH, exist_ok=True)

    # Sign into google calendar.
    service = google_calendar.build_service()

    # Get the moodle calendar.
    moodle_url = menu.input_moodle_url()
    utility.download_calendar_file(moodle_url, moodle.moodle_filepath)

    # Get the filters.
    exclusive_filters = menu.input_moodle_event_filters()
    filtered_events = moodle.filter_calendar(moodle.moodle_filepath, exclusive_filters)

    # Get the desired calendar.
    calendar_id = menu.input_google_calendar_id(service)

    # Put filtered events onto google calendar.
    google_calendar.add_events(service, calendar_id, filtered_events)

    menu.script_done()

if __name__ == "__main__":
    main()