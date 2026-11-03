
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
                    Version 0.5
    """)


def print_scan_info(target, target_ip, start, end):
    """
    Display information before scanning.
    """

    print(f"\n[# Scanning Target] {target}")
    print(f"[# Resolved IP] {target_ip}")
    print(f"[# Port Range] {start}-{end}")


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
        print(
            f"{result['port']:<10}"
            f"{result['registered_service']:<15}"
            f"{result['detected_service']:<18}"
            f"{result['status']:<10}"
            f"{result['banner'][:100]}"
        )

    print("-" * 100)

    print(f"Total ports scanned : {results['total_scanned']}")
    print(f"Open ports found    : {len(open_ports)}")
    print(f"Scan duration       : {results['duration']:.2f} seconds")

    print("=" * 100 + "\n")


def print_error(message):
    """
    Display an error message.
    """

    print(f"\n[!] {message}")
