import os
import subprocess
import sys


TEMP_DIRECTORY_PATH = "temp"
CONFIG_DIRECTORY_PATH = "config"
REQUIREMENTS_FILENAME = "requirements.txt"


def install_package(pypi_name):
    """Installs a package using pip."""
    print(f"Installing {pypi_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pypi_name])

def install_missing_packages():
    requirements_filepath = os.path.join(CONFIG_DIRECTORY_PATH, REQUIREMENTS_FILENAME)

    with open(requirements_filepath) as requirements:
        for requirement in requirements:
            requirement = requirement.strip()

            # Skip empty lines.
            if not requirement:
                continue

            try:
                pypi_name, import_name = [x.strip() for x in requirement.split(",")]
            except ValueError:
                print(f"Skipping malformed line: {requirement}")
                continue

            try:
                __import__(import_name)
                print(f"{import_name} is already installed.")
            except ImportError:
                install_package(pypi_name)

# NOTE This runs every time this module is imported. It needs to be this way so that missing packages are installed prior to attempting to import them in main.py.
install_missing_packages()