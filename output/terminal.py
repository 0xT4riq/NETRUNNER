
import sys
import time



class ProgressDisplay:
    """
    Display scan progress, speed, and estimated completion time.
    """

    def __init__(self, width=24, refresh_interval=0.1):
        self.width = width
        self.refresh_interval = refresh_interval
        self.last_update = 0

    def update(self, completed, total, elapsed):
        """Update the progress bar."""

        if total <= 0:
            return

        now = time.perf_counter()

        # Avoid refreshing the terminal too frequently.
        if (
            now - self.last_update < self.refresh_interval
            and completed < total
        ):
            return

        self.last_update = now

        percentage = completed / total * 100

        filled = int(self.width * completed / total)
        bar = "━" * filled + "░" * (self.width - filled)

        speed = completed / elapsed if elapsed > 0 else 0

        remaining = total - completed
        eta_seconds = remaining / speed if speed > 0 else 0

        hours = int(eta_seconds // 3600)
        minutes = int((eta_seconds % 3600) // 60)
        seconds = int(eta_seconds % 60)

        eta = (
            f"{hours:02}:{minutes:02}:{seconds:02}"
            if speed > 0
            else "--:--:--"
        )

        message = (
            f"\rScanning {bar} {percentage:5.1f}% | "
            f"{completed:,}/{total:,} ports | "
            f"Elapsed: {elapsed:.1f}s | "
            f"ETA: {eta}"
        )

        sys.stdout.write("\r\033[K" + message)
        sys.stdout.flush()

        if completed == total:
            print()


def print_banner():
    """
    Display NETRUNNER logo and version.
    """

    print(r"""
 _   _ _____ _____ ____  _   _ _   _ _   _ _____ ____
| \ | | ____|_   _|  _ \| | | | \ | | | | | ____|  _ \
|  \| |  _|   | | |_) | | | |  \| | | | |  _| | |_) |
| |\  | |___  | | |  _ <| |_| | |\  | |_| | |___|  _ <
|_| \_|_____| |_| |_| \_\\____/|_| \_|\___/|_____|_| \_\\

             Network Reconnaissance Tool
                       NETRUNNER v1.1.0

                 Developed by 0xT4riq
              github.com/0xT4riq/NETRUNNER

             Copyright (c) 2026 0xT4riq
    """)



def print_scan_info(target, target_ip, ports, end=None):
    """
    Display information before scanning.
    """

    if end is not None:
        selected_ports = list(range(ports, end + 1))
    else:
        selected_ports = sorted(set(ports))

    print(f"\n[# Scanning Target] {target}")
    print(f"[# Resolved IP] {target_ip}")

    if len(selected_ports) <= 20:
        print(f"[# Selected Ports] {', '.join(map(str, selected_ports))}")
    else:
        print(f"[# Selected Ports] {len(selected_ports)} ports")
        print(
            f"[# Port Span] "
            f"{selected_ports[0]}-{selected_ports[-1]}"
        )



def print_open_ports(results):
    """
    Display discovered open ports.
    """

    open_ports = results["open_ports"]

    print("\n" + "=" * 100)
    print(f" NETRUNNER | SCAN RESULTS FOR {results['hostname']}")
    print("=" * 100)

    print(
        f"{'PORT':<10}"
        f"{'REGISTERED':<15}"
        f"{'DETECTED':<18}"
        f"{'STATUS':<10}"
        f"BANNER"
    )

    print("-" * 100)

    for result in open_ports:
        banner = result.get("banner") or ""
        first_line = banner.splitlines()[0][:100] if banner else "N/A"

        print(
            f"{result['port']:<10}"
            f"{result['registered_service']:<15}"
            f"{result['detected_service']:<18}"
            f"{result['status']:<10}"
            f"{first_line}"
        )

    print("-" * 100)

    duration = results["duration"]
    total_scanned = results["total_scanned"]

    average_speed = (
        total_scanned / duration
        if duration > 0
        else 0
    )

    print("\n[SCAN SUMMARY]")
    print(f"Target              : {results['hostname']}")
    print(f"Resolved IP         : {results['target_ip']}")
    print(f"Total ports scanned : {total_scanned:,}")
    print(f"Open ports found    : {len(open_ports):,}")
    print(f"Scan duration       : {duration:.2f} seconds")
    print(f"Average scan speed  : {average_speed:,.2f} ports/sec")

    if not open_ports:
        print("Result              : No open ports discovered")

    print("=" * 100 + "\n")

def print_tls_results(results):
    """Display TLS inspection results."""

    print("\n" + "=" * 70)
    print(f" NETRUNNER | TLS INSPECTION FOR {results['hostname']}")
    print("=" * 70)

    for port_result in results["open_ports"]:
        tls = port_result.get("tls")

        if tls is None:
            continue

        print(f"\n[PORT {tls['port']}]")

        if not tls["tls_supported"]:
            print("TLS Supported       : No")
            print(f"Error               : {tls['error'] or 'TLS handshake failed'}")
            continue

        certificate = tls["certificate"]

        print("TLS Supported       : Yes")
        print(f"TLS Version         : {tls['tls_version']}")
        print(f"Cipher              : {tls['cipher']}")
        print(f"Certificate Verified: {tls['certificate_verified']}")

        if tls["verification_error"]:
            print(f"Verification Error  : {tls['verification_error']}")

        if certificate:
            print(f"Subject             : {certificate['subject']}")
            print(f"Issuer              : {certificate['issuer']}")
            print(f"Valid From          : {certificate['valid_from']}")
            print(f"Valid Until         : {certificate['valid_until']}")
            print(f"Validity Status     : {certificate['validity_status']}")
            print(f"Days Remaining      : {certificate['days_remaining']}")
            print(f"SHA256 Fingerprint  : {certificate['fingerprint_sha256']}")

        san_domains = certificate.get("san_domains", [])
        for domain in san_domains[:5]:  # Limit to first 5 SAN domains
            print(f"SAN Domain          : {domain}")
        remaining_sans = len(san_domains) - 5
        if remaining_sans > 0:
            print(f"... and {remaining_sans} more SAN domains")

    print("\n" + "=" * 70)

def print_error(message):
    """
    Display an error message.
    """

    print(f"\n[!] {message}")


def ask_export():

    print("\n[?] Export scan results?")
    print("1. JSON")
    print("2. CSV")
    print("3. Both")
    print("4. Skip")

    choice = input("[+] Select an option: ").strip()

    return choice
