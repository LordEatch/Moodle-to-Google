import os
import pkg_resources
import subprocess
import sys


TEMP_DIRECTORY_PATH = "temp"
CONFIG_DIRECTORY_PATH = "config"
REQUIREMENTS_FILENAME = "requirements.txt"


def package_installed(package_name):
    """Check if a package is already installed."""

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    return package_name.lower() in installed_packages

def install_package(package_name):
    if package_installed(package_name):
        raise Exception(f"Package '{package_name}' is already installed.")

    try:
        print(f"Installing package: {package_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Package '{package_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package '{package_name}'. Error: {e}")

def get_required_packages(filename):
    with open(filename) as requirements:
        return [line.strip() for line in requirements.readlines()]

def install_missing_packages():
    requirements_path = os.path.join(CONFIG_DIRECTORY_PATH, REQUIREMENTS_FILENAME)

    requirements = get_required_packages(requirements_path)

    for package in requirements:
        if not package_installed(package):
            print(f"\tInstalling package: {package}...")
            install_package(package)

# NOTE This runs every time this module is imported. It needs to be this way so that missing packages are installed prior to attempting to import them in main.py.
install_missing_packages()