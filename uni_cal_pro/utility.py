import requests


def is_calendar_file(url):
    """
    Checks if the file at the given URL has a .ics MIME type without downloading the full file.
    Returns True if it's an .ics file, False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get("Content-Type", "")
        is_calendar = "text/calendar" in content_type

        if is_calendar:
            return True
        else:
            print(f"\tValid url but invalid file type: {content_type}")
            return False
    except Exception as e:
        print(f"\t{e}")
        return False

def download_calendar_file(url, filepath):
    """
    Downloads the file from the given URL and saves it with the given filename.
    Only downloads if the MIME type is 'text/calendar'.
    """
    if not is_calendar_file(url):
        print("\tThe file is not a calendar file. Skipping download.")
        return False

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Save the file.
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"\tFile downloaded successfully at {filepath}")
        return True
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return False