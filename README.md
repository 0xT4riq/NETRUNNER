# NETRUNNER

**A Python-based TCP Network Reconnaissance Tool**

NETRUNNER is a command-line network reconnaissance tool built with Python. It scans TCP ports, identifies open services, collects service banners, and exports scan results in JSON and CSV formats.

This project was developed as a hands-on learning experience to strengthen my understanding of Python, computer networking, socket programming, concurrency, and software testing.

## Features

- **Target Resolution:** Accepts IPv4 addresses and hostnames.
- **TCP Port Scanning:** Checks a specified range of TCP ports.
- **Concurrent Scanning:** Uses Python's `ThreadPoolExecutor` to scan multiple ports simultaneously.
- **Service Identification:** Identifies services using registered port information and basic banner inspection.
- **Banner Grabbing:** Collects available service banners and HTTP responses.
- **Terminal Interface:** Displays scan results in a structured format.
- **Report Export:** Saves results as JSON and CSV files.
- **Automated Testing:** Includes unit tests and an integration test using a local TCP server.

## Project Structure

```text
portScanner/
│
├── main.py
├── config.py
├── core/
│   ├── scanner.py
│   ├── target.py
│   └── validator.py
│
├── detection/
│   └── services.py
│
├── output/
│   ├── terminal.py
│   └── reports.py
│
├── tests/
│   ├── test_reports.py
│   ├── test_scanner.py
│   ├── test_services.py
│   ├── test_target.py
│   └── test_validator.py
│
└── README.md
```

## Requirements

- Python 3.10 or later
- No third-party Python packages required.

NETRUNNER currently uses Python's standard library.

## Installation

Clone the repository:

```bash
git clone https://github.com/0xT4riq/NETRUNNER.git
```

Navigate to the project directory:

```bash
cd NETRUNNER
```

Run the application:

```bash
python main.py
```

## Usage

When launched, NETRUNNER asks for:

1. Target IP address or hostname.
2. TCP port range.

Example:

```text
[+] Enter target/s (separate with commas): 127.0.0.1
[+] Enter port range (e.g. 20-80) or leave empty: 1-1000
```

You can enter multiple targets separated by commas.

Leaving the port range empty scans ports 1–65535.

After scanning, NETRUNNER displays discovered open ports and offers JSON and CSV export options.

## Example Results

Example output from an authorized scan of `scanme.nmap.org`:

```text
PORT      REGISTERED     DETECTED          STATUS
---------------------------------------------------
22        ssh            SSH               Open
80        http           HTTP              Open
---------------------------------------------------
Total ports scanned : 1000
Open ports found    : 2
Scan duration       : 10.26 seconds
```

Scan results can be exported as:

- JSON: Includes target information, scan metadata, and open-port details.
- CSV: Contains open-port details for spreadsheet analysis.

## Running Tests

NETRUNNER includes automated tests using Python's built-in `unittest` framework.

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The current test suite contains **19 tests** covering:

- Port-range validation.
- Target validation and hostname resolution.
- Service banner identification.
- TCP scanning against a local test server.
- JSON and CSV report generation.

## Current Limitations

NETRUNNER is an educational project and has some limitations:

- Supports IPv4 TCP scanning; IPv6 scanning is not implemented.
- Service identification relies on basic banner inspection and registered port information.
- Banner collection is not supported for every protocol.
- HTTPS/TLS-specific service inspection is not implemented.
- It does not currently perform UDP scanning or operating-system fingerprinting.

## Responsible Use

NETRUNNER is intended for educational purposes and authorized network testing.

Only scan systems and networks you own or have explicit permission to test. The developer is not responsible for unauthorized use of this tool.

## Future Improvements

Potential future enhancements include:

- Improved service fingerprinting.
- HTTPS/TLS banner inspection.
- UDP scanning.
- Better scan cancellation and task management.
- Improved terminal output and reporting.
- Additional automated tests.

## Author

Developed as a personal cybersecurity and Python learning project.

**NETRUNNER — Explore. Scan. Understand.**