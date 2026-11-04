# NETRUNNER

**A lightweight TCP network reconnaissance tool built with Python.**

NETRUNNER is an open-source command-line tool designed to simplify TCP port scanning and basic service identification. It supports concurrent scanning, predefined port profiles, banner grabbing, and exporting scan results.

Built as a practical cybersecurity project, NETRUNNER aims to make network reconnaissance simple, accessible, and extensible.

<p align="center">
  <strong>Version 1.1.0</strong>
</p>

---

## Features

- **TCP Port Scanning** – Scan individual ports, custom ranges, or all TCP ports.
- **Concurrent Scanning** – Scan multiple ports simultaneously using Python threads.
- **Port Profiles** – Quickly select predefined scanning profiles.
- **Multiple Targets** – Scan multiple IP addresses or hostnames.
- **Service Identification** – Identify common services using registered port information and basic banner detection.
- **Banner Grabbing** – Collect service response banners where available.
- **Live Progress** – Monitor scan progress, scanning speed, and estimated completion time.
- **Scan Summary** – View scan statistics, including duration, open ports, and average speed.
- **Report Export** – Save scan results in JSON or CSV format.
- **Command-Line Interface** – Run scans directly from your terminal.
- **Interactive Mode** – Use NETRUNNER without remembering command arguments.

## Installation

### Requirements

- Python 3.10 or newer
- Git

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

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install NETRUNNER

```bash
pip install -e .
```

### 4. Verify installation

```bash
netrunner --version
netrunner --help
```

## Usage

NETRUNNER supports both command-line and interactive usage.

### Basic scanning

Scan a target using the default port range:

```bash
netrunner scan 192.168.1.1
```

### Custom port selection

Scan a single port:

```bash
netrunner scan 192.168.1.1 -p 80
```

Scan multiple ports:

```bash
netrunner scan 192.168.1.1 -p 22,80,443
```

Scan a specific range:

```bash
netrunner scan 192.168.1.1 -p 1-1000
```

Combine individual ports and ranges:

```bash
netrunner scan 192.168.1.1 -p 22,80,443,8000-8100
```

## Port Profiles

NETRUNNER includes predefined profiles to make common scanning tasks easier.

| Profile | Description |
|---|---|
| `quick` | A selection of commonly used TCP ports |
| `web` | Common HTTP, HTTPS, and alternative web ports |
| `full` | All TCP ports (1–65535) |

**Quick scan:**

```bash
netrunner scan 192.168.1.1 --profile quick
```

**Web scan:**

```bash
netrunner scan 192.168.1.1 --profile web
```

**Full TCP scan:**

```bash
netrunner scan 192.168.1.1 --profile full
```

Profiles and custom port selections are mutually exclusive. Use either `--profile` or `--ports` for a scan.

## Multiple Targets

Scan multiple targets in one command:

```bash
netrunner scan 192.168.1.1 192.168.1.2
```

You can also separate targets using commas:

```bash
netrunner scan 192.168.1.1,192.168.1.2
```

### Exporting Results

NETRUNNER supports three export options:

**JSON:**

```bash
netrunner scan 192.168.1.1 --profile quick --format json
```

**CSV:**

```bash
netrunner scan 192.168.1.1 --profile quick --format csv
```

**Both formats:**

```bash
netrunner scan 192.168.1.1 --profile quick --format both
```

Reports are saved in the `reports/` directory.

## Interactive Mode

You can also launch NETRUNNER without arguments:

```bash
netrunner
```

Follow the prompts to enter your target, select ports, and optionally export the results.

## Example Output

During a scan, NETRUNNER displays live progress, scanning speed, and estimated completion time.

```text
Scan [━━━━━━━━━━░░░░░░░░░░]  50.0% | 500/1,000 | 85 p/s | ETA 00:00:05
```

After scanning, NETRUNNER displays a summary containing:

- Target and resolved IP address
- Total ports scanned
- Number of open ports discovered
- Scan duration
- Average scanning speed

*Output and performance will vary depending on the target and network conditions.*

## Running Tests

To run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Current Limitations

NETRUNNER is actively being developed. Its current limitations include:

- IPv4-focused scanning.
- TCP scanning only; UDP scanning is not supported.
- Basic service identification based on registered ports and response banners.
- No operating system fingerprinting.
- No dedicated TLS/HTTPS inspection.
- Service identification may be incomplete when services do not provide recognizable banners.

## Roadmap

Future development may include:

- Improved service fingerprinting.
- HTTPS/TLS inspection.
- IPv6 support.
- UDP scanning.
- More reconnaissance capabilities.
- Additional output and reporting options.

## Responsible Use

NETRUNNER is intended for educational purposes, network administration, and authorized security testing.

**Only scan systems and networks that you own or have explicit permission to test.**

The developer is not responsible for misuse of this tool.

## Contributing

Contributions, bug reports, and feature suggestions are welcome!

If you find a bug or have an idea that could improve NETRUNNER, feel free to open an issue or submit a pull request.

## Author

**0xT4riq**

GitHub: https://github.com/0xT4riq

Project: https://github.com/0xT4riq/NETRUNNER

---

*NETRUNNER — Learn, Build, Recon.*