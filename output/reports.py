
import json
import csv
import os

from datetime import datetime


REPORTS_DIR = "reports"


def create_reports_directory():
    """Create reports directory if it doesn't exist."""

    os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_filename(extension):
    """Generate a unique report filename."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"netrunner_{timestamp}.{extension}"


def save_json(results):
    """Save scan results as JSON."""

    create_reports_directory()

    filename = generate_filename("json")
    filepath = os.path.join(REPORTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    return filepath


def save_csv(results):
    """Save discovered open ports as CSV."""

    create_reports_directory()

    filename = generate_filename("csv")
    filepath = os.path.join(REPORTS_DIR, filename)

    open_ports = results["open_ports"]

    fieldnames = [
        "port",
        "status",
        "registered_service",
        "detected_service",
        "banner"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(open_ports)

    return filepath
