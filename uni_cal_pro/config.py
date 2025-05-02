from importlib import util
import os
import subprocess
import sys


TEMP_DIRECTORY_PATH = "temp"
CONFIG_DIRECTORY_PATH = "config"
REQUIREMENTS_FILENAME = "requirements.txt"


def package_installed(package_name):
    """Check if a package is already installed."""

    return util.find_spec(package_name) is not None

def install_package(package_name):
    if package_installed(package_name):
        print(f"Package '{package_name}' is already installed.")
        return

    try:
        print(f"Installing package: {package_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Package '{package_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package '{package_name}'. Error: {e}")

def get_required_packages(filename):
    with open(filename) as requirements:
        return requirements.readlines()

def install_missing_packages():
    requirements_path = os.path.join(CONFIG_DIRECTORY_PATH, REQUIREMENTS_FILENAME)

    requirements = get_required_packages(requirements_path)

    for package in requirements:
        install_package(package)