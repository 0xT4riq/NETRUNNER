
import socket
import time
import concurrent.futures

from config import MAX_WORKERS, CONNECT_TIMEOUT
from detection.services import (
    get_registered_service,
    detect_service,
    grab_banner
)


def scan_port(target_ip, hostname, port):
    """
    Attempt a TCP connection to one port.
    Returns a dictionary if open, otherwise None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(CONNECT_TIMEOUT)

            try:
                sock.connect((target_ip, port))
            except OSError:
                return None

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



def scan(target_ip, hostname, ports, end_port=None, progress_callback=None):
    """
    Scan selected TCP ports concurrently.

    Reports progress through an optional callback.
    """

    if end_port is not None:
        ports = range(ports, end_port + 1)

    ports = sorted(set(ports))

    if not ports:
        raise ValueError("At least one port must be selected.")

    open_ports = []
    futures = []

    total_ports = len(ports)
    completed = 0

    start_time = time.perf_counter()

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    )

    try:
        for port in ports:
            future = executor.submit(
                scan_port,
                target_ip,
                hostname,
                port
            )
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            if result:
                open_ports.append(result)

            completed += 1

            elapsed = time.perf_counter() - start_time

            if progress_callback:
                progress_callback(
                    completed,
                    total_ports,
                    elapsed
                )

    finally:
        executor.shutdown(wait=True, cancel_futures=True)

    elapsed = time.perf_counter() - start_time

    return {
        "target_ip": target_ip,
        "hostname": hostname,
        "ports": ports,
        "open_ports": sorted(
            open_ports,
            key=lambda result: result["port"]
        ),
        "total_scanned": total_ports,
        "duration": elapsed
    }
