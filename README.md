# NETRUNNER

**A lightweight TCP network reconnaissance tool built with Python.**

NETRUNNER is an open-source command-line tool for scanning TCP ports, identifying services, collecting service banners, and exporting scan results.

Developed by [0xT4riq](https://github.com/0xT4riq).

---

## Features

- TCP port scanning
- Concurrent scanning using Python threads
- Scan multiple targets
- Custom port selection and ranges
- Basic service identification
- Banner grabbing
- Live scan progress, speed, and ETA
- JSON and CSV report export
- Interactive and command-line interfaces

## Requirements

- Python 3.10 or newer
- Windows, Linux, or macOS

No third-party runtime dependencies are required.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/0xT4riq/NETRUNNER.git
cd NETRUNNER
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install NETRUNNER

```bash
python -m pip install -e .
```

## Usage

After installation, run NETRUNNER directly from your terminal.

### Help

```bash
netrunner -h
netrunner --help
```

View scan-specific options:

```bash
netrunner scan -h
```

### Version

```bash
netrunner --version
```

### Basic scan

```bash
netrunner scan 192.168.1.1
```

### Scan selected ports

```bash
netrunner scan 192.168.1.1 -p 80
```

### Scan multiple ports

```bash
netrunner scan 192.168.1.1 -p 22,80,443
```

### Scan a port range

```bash
netrunner scan 192.168.1.1 -p 1-1000
```

### Scan multiple targets

```bash
netrunner scan 192.168.1.1 192.168.1.2 -p 22,80,443
```

Comma-separated targets are also supported:

```bash
netrunner scan 192.168.1.1,192.168.1.2 -p 80
```

### Export results

Export as JSON:

```bash
netrunner scan 192.168.1.1 -p 1-1000 --format json
```

Export as CSV:

```bash
netrunner scan 192.168.1.1 -p 1-1000 --format csv
```

Export both formats:

```bash
netrunner scan 192.168.1.1 -p 1-1000 --format both
```

Reports are saved in the `reports/` directory.

### Interactive mode

You can also start NETRUNNER without arguments:

```bash
netrunner
```

Or run it directly from the source:

```bash
python main.py
```

## Example output

```text
NETRUNNER v1.0.0

[+] Target: 192.168.1.1

Scanning ━━━━━━━━━━━━━━━━━━━━ 100.0%
1,000/1,000 ports | 2,450 ports/sec

NETRUNNER | SCAN SUMMARY

Total ports scanned : 1,000
Open ports found    : 3
Elapsed time        : 0.41 seconds
```

*Example output is illustrative.*

## Running tests

Run the project's test suite:

```bash
python -m unittest discover -s tests -v
```

## Current limitations

NETRUNNER is currently focused on TCP reconnaissance.

- IPv4 scanning only.
- No UDP scanning.
- No operating-system fingerprinting.
- Basic service identification based on banners.
- No dedicated TLS/HTTPS inspection.

## Responsible use

NETRUNNER is intended for educational purposes and authorized network reconnaissance.

Only scan systems and networks that you own or have explicit permission to test. You are responsible for complying with applicable laws and network policies.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

Please open an issue before starting major changes so we can discuss the proposed improvement.

## License

NETRUNNER is intended to be distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Developed by [0xT4riq](https://github.com/0xT4riq)**

[GitHub Repository](https://github.com/0xT4riq/NETRUNNER)