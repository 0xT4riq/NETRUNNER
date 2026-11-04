
import argparse
import signal
import sys

from core.target import check_ip
from core.validator import validate_port_range, parse_ports
from core.scanner import scan

from detection.services import detect_service
from output.terminal import (
    print_banner,
    print_scan_info,
    print_open_ports,
    print_error,
    ask_export,
    ProgressDisplay,
    print_tls_results
)
from detection.tls import inspect_tls
from output.reports import save_json, save_csv
from config import DEFAULT_START_PORT, DEFAULT_END_PORT, VERSION, PORT_PROFILES




def shutdown(sig, frame):
    print("\n\n[!] NETRUNNER terminated by user.")
    sys.exit(0)



def export_results(results, export_format):
    """Export scan results in the selected format."""

    try:
        if export_format == "json":
            print(f"[+] JSON report saved: {save_json(results)}")

        elif export_format == "csv":
            print(f"[+] CSV report saved: {save_csv(results)}")

        elif export_format == "both":
            print(f"[+] JSON report saved: {save_json(results)}")
            print(f"[+] CSV report saved: {save_csv(results)}")

        return True

    except OSError as error:
        print_error(f"Could not save report: {error}")
        return False


def run_scan(targets, ports, export_format=None, tls=False):
    """Run scans against one or more targets."""

    failed = False

    for target in targets:
        try:
            target_ip = check_ip(target)

            print_scan_info(target, target_ip, ports)

            progress = ProgressDisplay()

            progress.update(0, len(ports), 0)

            results = scan(
                target_ip,
                target,
                ports,
                progress_callback=progress.update
            )
            if tls:
                print("\n[+] Starting TLS inspection...")

                for port_result in results["open_ports"]:
                    tls_result = inspect_tls(
                        target,
                        port_result["port"]
                    )

                    port_result["tls"] = tls_result
                    if tls_result["tls_supported"]:
                        port_result["detected_service"] = detect_service(
                            port_result.get("banner", ""),
                            tls_supported=True,
                            registered_service=port_result["registered_service"]
                        )


                print_tls_results(results)

            print_open_ports(results)

            if export_format:
                if not export_results(results, export_format):
                    failed = True

            elif sys.stdin.isatty():
                choice = ask_export()

                formats = {
                    "1": "json",
                    "2": "csv",
                    "3": "both"
                }

                if choice in formats:
                    if not export_results(results, formats[choice]):
                        failed = True

                elif choice == "4":
                    print("[+] Export skipped.")

                else:
                    print("[!] Invalid selection.")

        except (ValueError, OSError) as error:
            print_error(f"{target}: {error}")
            failed = True

    return 1 if failed else 0



def interactive_mode():
    """Run NETRUNNER using the original interactive interface."""

    print_banner()

    targets_input = input(
        "[+] Enter target/s (separate with commas): "
    ).strip()

    port_range = input(
        "[+] Enter port range (e.g. 20-80) or leave empty: "
    ).strip()

    try:
        if port_range:
            start_port, end_port = map(int, port_range.split("-"))
        else:
            start_port = DEFAULT_START_PORT
            end_port = DEFAULT_END_PORT

        validate_port_range(start_port, end_port)

        ports = list(range(start_port, end_port + 1))

    except ValueError as error:
        print_error(f"Invalid port range: {error}")
        return

    targets = [
        target.strip()
        for target in targets_input.split(",")
        if target.strip()
    ]

    if not targets:
        print_error("No targets provided.")
        return

    return run_scan(targets, ports)


def build_parser():
    """Configure NETRUNNER command-line arguments."""

    parser = argparse.ArgumentParser(
        prog="netrunner",
        description="NETRUNNER - Python Network Reconnaissance Tool"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"NETRUNNER {VERSION}"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan one or more targets"
    )

    scan_parser.add_argument(
        "targets",
        nargs="+",
        help="Target IP addresses or hostnames"
    )

    scan_parser.add_argument(
        "-p",
        "--ports",
        default=f"{DEFAULT_START_PORT}-{DEFAULT_END_PORT}",
        help="Ports to scan (example: 22,80,443 or 1-1000)"
    )
    scan_parser.add_argument(
        "--profile",
        choices=["quick", "web", "full"],
        help="Choose a predefined port scanning profile"
    )
    scan_parser.add_argument(
        "--tls",
        action="store_true",
        help="Inspect TLS certificates on open ports"
    )

    scan_parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        help="Automatically export scan results"
    )

    return parser



def main():
    signal.signal(signal.SIGINT, shutdown)

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        interactive_mode()
        return 0

    if args.command == "scan":
        try:
            if args.profile:
                if args.ports != f"{DEFAULT_START_PORT}-{DEFAULT_END_PORT}":
                    parser.error("Use either --profile or --ports, not both.")

                ports = PORT_PROFILES[args.profile]

            else:
                ports = parse_ports(args.ports)

            targets = []

            for target in args.targets:
                targets.extend(
                    item.strip()
                    for item in target.split(",")
                    if item.strip()
                )

            if not targets:
                parser.error("At least one target must be provided.")

            print_banner()

            return run_scan(
                targets,
                ports,
                args.format,
                tls=args.tls
            )

        except ValueError as error:
            parser.error(str(error))

    return 0


if __name__ == "__main__":
    sys.exit(main())

