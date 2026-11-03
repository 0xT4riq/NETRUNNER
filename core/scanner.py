
import socket
import time
import concurrent.futures

from config import (
    MAX_WORKERS,
    CONNECT_TIMEOUT,
    BANNER_TIMEOUT,
    HTTP_PORTS
)
from detection.services import (
    get_registered_service,
    detect_service,
    grab_banner
)



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

            # TCP connection succeeded.
            registered_service = get_registered_service(port)

            # Separate timeout for banner collection.
            sock.settimeout(BANNER_TIMEOUT)


            registered_service = get_registered_service(port)

            banner = grab_banner(sock, hostname, port)

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


def scan(target_ip, hostname, start_port, end_port):
    """
    Scan a range of TCP ports concurrently.

    Returns a list containing information about open ports.
    """

    open_ports = []
    futures = []

    start_time = time.perf_counter()

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    )

    try:

        # Submit scanning tasks.
        for port in range(start_port, end_port + 1):

            future = executor.submit(
                scan_port,
                target_ip,
                hostname,
                port
            )

            futures.append(future)

        # Collect results as tasks finish.
        for future in concurrent.futures.as_completed(futures):

            result = future.result()

            if result:
                open_ports.append(result)

    except KeyboardInterrupt:

        print("\n[!] Scan interrupted.")

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

    return {
        "target_ip": target_ip,
        "hostname": hostname,
        "start_port": start_port,
        "end_port": end_port,
        "open_ports": sorted(
            open_ports,
            key=lambda result: result["port"]
        ),
        "total_scanned": end_port - start_port + 1,
        "duration": elapsed
    }
