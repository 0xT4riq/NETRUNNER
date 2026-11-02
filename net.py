import socket
import ipaddress
import time
import threading
import concurrent.futures
import signal
import sys


def shutdown(sig, frame):
  print("\nGracefully shutting down...")
  sys.exit(0)

signal.signal(signal.SIGINT, shutdown)


  
def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

def scan_port(ipaddress, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((ipaddress, port))

            data = sock.recv(1024)
            if not data:
                request = (
                    f"HEAD / HTTP/1.1\r\n"
                    f"Host: {hostname}\r\n"
                    f"Connection: close\r\n\r\n"
                )
                sock.sendall(request.encode())
                data = sock.recv(1024)
            banner = data.decode('utf-8', errors='ignore').strip()
            try:
                service = socket.getservbyport(port, "tcp")
            except (OSError, socket.error):
                service = "Unknown"

            return {
                "port": port,
                "status": "open",
                "banner": banner if banner else "No banner received",
                "service": service
            }
    except OSError:
        return None
def print_open_ports(open_ports, target, start, end):
    print("\n" + "=" * 65)
    print(f" NETRUNNER | SCAN RESULTS FOR {target}")
    print("=" * 65)

    print(f"{'PORT':<10} {'SERVICE':<12} {'STATUS':<12} {'BANNER'}")
    print("-" * 65)
    open_ports.sort(key=lambda x: x["port"])
    for result in open_ports:
        print(
            f"{result['port']:<10} "
            f"{result['service']:<12} "
            f"{result['status'].upper():<12} "
            f"{result['banner']}"
        )

    print("-" * 65)
    print(f"Total ports scanned : {end - start + 1}")
    print(f"Open ports found    : {len(open_ports)}")
    print("=" * 65 + "\n")

def scan(target,start,end):
    open_ports = []
    futures = []   
    converted_ip = check_ip(target)
    print('\n' + '[# Scanning Target]---- ' + str(target))
    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start, end + 1):
            future = executor.submit(scan_port, converted_ip, port)
            futures.append(future)
        pass
    for future in futures:
        result = future.result()
        if result:
            open_ports.append(result)
    elapsed = time.perf_counter() - start_time
    print(f"Scan duration       : {elapsed:.2f} seconds")
    print_open_ports(open_ports, target, start, end)

targets = input("[+] Enter target/s to scan (split multiple targets with ','): ")
port_range = input("[+] Enter the port range to scan (e.g. 20-80) or leave it empty: ")

if '-' in port_range:
    start_port, end_port = map(int, port_range.split('-'))
else:
    start_port, end_port = 1, 65535

if ',' in targets:
    for target in targets.split(','):
        scan(target.strip(), start_port, end_port)
else:
    scan(targets, start_port, end_port)
