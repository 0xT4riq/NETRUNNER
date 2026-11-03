
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
                       NETRUNNER v1.0.0

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
        print(
            f"{result['port']:<10}"
            f"{result['registered_service']:<15}"
            f"{result['detected_service']:<18}"
            f"{result['status']:<10}"
            f"{result['banner'].splitlines()[0][:100]}"
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


def ask_export():

    print("\n[?] Export scan results?")
    print("1. JSON")
    print("2. CSV")
    print("3. Both")
    print("4. Skip")

    choice = input("[+] Select an option: ").strip()

    return choice
