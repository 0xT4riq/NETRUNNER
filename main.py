
import signal
import sys

from core.target import check_ip
from core.validator import validate_port_range
from core.scanner import scan

from output.terminal import (
    print_banner,
    print_scan_info,
    print_open_ports,
    print_error
)

from config import DEFAULT_START_PORT, DEFAULT_END_PORT


def shutdown(sig, frame):
    print("\n\n[!] NETRUNNER terminated by user.")
    sys.exit(0)


def main():

    signal.signal(signal.SIGINT, shutdown)

    print_banner()

    # Get user input
    targets_input = input(
        "[+] Enter target/s (separate with commas): "
    ).strip()

    port_range = input(
        "[+] Enter port range (e.g. 20-80) or leave empty: "
    ).strip()

    # Validate and parse port range
    try:

        if port_range:
            start_port, end_port = map(
                int,
                port_range.split("-")
            )

        else:
            start_port = DEFAULT_START_PORT
            end_port = DEFAULT_END_PORT

        validate_port_range(start_port, end_port)

    except ValueError as error:
        print_error(f"Invalid port range: {error}")
        return

    # Parse targets
    targets = [
        target.strip()
        for target in targets_input.split(",")
        if target.strip()
    ]

    if not targets:
        print_error("No targets provided.")
        return

    # Scan each target
    for target in targets:

        try:
            target_ip = check_ip(target)

            print_scan_info(
                target,
                target_ip,
                start_port,
                end_port
            )

            results = scan(
                target_ip,
                target,
                start_port,
                end_port
            )

            if results:
                print_open_ports(results)

        except ValueError as error:
            print_error(str(error))


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n\n[!] NETRUNNER terminated by user.")
