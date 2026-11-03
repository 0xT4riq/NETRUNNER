
import socket
import ipaddress
import time
import concurrent.futures


# ==============================
# NETRUNNER CONFIGURATION
# ==============================

MAX_WORKERS = 100
CONNECT_TIMEOUT = 1
BANNER_TIMEOUT = 0.7

# Only send HTTP requests to common HTTP ports.
HTTP_PORTS = {80, 8000, 8008, 8080, 8888}


# ==============================
# TARGET VALIDATION
# ==============================

def check_ip(target):
    """
    Validate an IP address or resolve a hostname.
    Returns the resolved IPv4 address.
    """

    try:
        ipaddress.ip_address(target)
        return target

    except ValueError:
        try:
            return socket.gethostbyname(target)

        except socket.gaierror:
            raise ValueError(f"Invalid target or hostname: {target}")


def validate_port_range(start, end):
    """
    Check that the supplied port range is valid.
    """

    if not (1 <= start <= 65535):
        raise ValueError("Starting port must be between 1 and 65535.")

    if not (1 <= end <= 65535):
        raise ValueError("Ending port must be between 1 and 65535.")

    if start > end:
        raise ValueError("Starting port cannot be greater than ending port.")


# ==============================
# SERVICE IDENTIFICATION
# ==============================

def get_registered_service(port):
    """
    Get the conventional service name registered
    for a TCP port number.
    """

    try:
        return socket.getservbyport(port, "tcp")

    except OSError:
        return "Unknown"


def detect_service(banner):
    """
    Make a basic guess based on the received banner.
    This is not full service fingerprinting.
    """

    if not banner:
        return "Unknown"

    upper_banner = banner.upper()

    if upper_banner.startswith("SSH-"):
        return "SSH"

    elif upper_banner.startswith("HTTP/"):
        return "HTTP"

    elif upper_banner.startswith("220"):
        return "FTP/SMTP (Possible)"

    elif upper_banner.startswith("+OK"):
        return "POP3"

    elif upper_banner.startswith("* OK"):
        return "IMAP"

    return "Unknown"


# ==============================
# PORT SCANNING
# ==============================

def scan_port(target_ip, hostname, port):
    """
    Attempt a TCP connection to one port.

    Returns a dictionary if the port is open.
    Returns None if the connection fails.
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # Connection timeout
            sock.settimeout(CONNECT_TIMEOUT)

            try:
                sock.connect((target_ip, port))

            except OSError:
                return None

            # The TCP connection succeeded: port is open.
            registered_service = get_registered_service(port)

            # Use a separate timeout for banner collection.
            sock.settimeout(BANNER_TIMEOUT)

            data = b""

            try:
                if port in HTTP_PORTS:
                    # HTTP servers usually wait for a request.
                    request = (
                        f"HEAD / HTTP/1.1\r\n"
                        f"Host: {hostname}\r\n"
                        f"Connection: close\r\n\r\n"
                    )

                    sock.sendall(request.encode("ascii"))
                    data = sock.recv(1024)

                else:
                    # Some services send their banner automatically.
                    data = sock.recv(1024)

            except socket.timeout:
                # No banner received within the timeout.
                pass

            except OSError:
                # Connection closed or another socket error.
                pass

            banner = data.decode(
                "utf-8",
                errors="ignore"
            ).strip()

            detected_service = detect_service(banner)

            return {
                "port": port,
                "status": "Open",
                "registered_service": registered_service,
                "detected_service": detected_service,
                "banner": banner if banner else "No banner received"
            }

    except OSError:
        return None


# ==============================
# RESULTS DISPLAY
# ==============================

def print_open_ports(open_ports, target, start, end):

    print("\n" + "=" * 100)
    print(f" NETRUNNER | SCAN RESULTS FOR {target}")
    print("=" * 100)

    print(
        f"{'PORT':<10}"
        f"{'REGISTERED':<15}"
        f"{'DETECTED':<18}"
        f"{'STATUS':<10}"
        f"BANNER"
    )

    print("-" * 100)

    open_ports.sort(key=lambda result: result["port"])

    for result in open_ports:

        print(
            f"{result['port']:<10}"
            f"{result['registered_service']:<15}"
            f"{result['detected_service']:<18}"
            f"{result['status']:<10}"
            f"{result['banner'][:100]}"
        )

    print("-" * 100)

    total_scanned = end - start + 1

    print(f"Total ports scanned : {total_scanned}")
    print(f"Open ports found    : {len(open_ports)}")

    print("=" * 100 + "\n")


# ==============================
# MAIN SCANNER
# ==============================

def scan(target, start, end):

    open_ports = []
    futures = []

    try:
        target_ip = check_ip(target)

    except ValueError as error:
        print(f"\n[!] {error}")
        return open_ports

    print(f"\n[# Scanning Target] {target}")
    print(f"[# Resolved IP] {target_ip}")
    print(f"[# Port Range] {start}-{end}")

    start_time = time.perf_counter()

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    )

    try:
        # Submit all port scanning tasks.
        for port in range(start, end + 1):

            future = executor.submit(
                scan_port,
                target_ip,
                target,
                port
            )

            futures.append(future)

        # Collect results as individual tasks finish.
        for future in concurrent.futures.as_completed(futures):

            result = future.result()

            if result:
                open_ports.append(result)

    except KeyboardInterrupt:

        print("\n\n[!] Scan interrupted by user.")

        # Cancel tasks that have not started.
        for future in futures:
            future.cancel()

        executor.shutdown(
            wait=True,
            cancel_futures=True
        )

        return open_ports

    else:
        executor.shutdown(wait=True)

    elapsed = time.perf_counter() - start_time

    print(f"\nScan duration       : {elapsed:.2f} seconds")

    print_open_ports(
        open_ports,
        target,
        start,
        end
    )

    return open_ports


# ==============================
# PROGRAM ENTRY POINT
# ==============================

def main():

    print("""
 _   _ _____ _____ ____  _   _ _   _ _   _ _____ ____  
| \ | | ____|_   _|  _ \| | | | \ | | | | | ____|  _ \ 
|  \| |  _|   | | | |_) | | | |  \| | | | |  _| | |_) |
| |\  | |___  | | |  _ <| |_| | |\  | |_| | |___|  _ < 
|_| \_|_____| |_| |_| \_\\____/|_| \_|\___/|_____|_| \_\\

             Network Reconnaissance Tool
                    Version 0.5
    """)

    targets_input = input(
        "[+] Enter target/s (separate with commas): "
    ).strip()

    port_range = input(
        "[+] Enter port range (e.g. 20-80) or leave empty: "
    ).strip()

    # Parse port range.
    try:

        if port_range:
            start_port, end_port = map(
                int,
                port_range.split("-")
            )

        else:
            start_port, end_port = 1, 65535

        validate_port_range(start_port, end_port)

    except ValueError as error:
        print(f"\n[!] Invalid port range: {error}")
        return

    # Parse targets.
    targets = [
        target.strip()
        for target in targets_input.split(",")
        if target.strip()
    ]

    if not targets:
        print("\n[!] No targets provided.")
        return

    # Scan each target.
    for target in targets:

        scan(
            target,
            start_port,
            end_port
        )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n\n[!] NETRUNNER terminated by user.")
