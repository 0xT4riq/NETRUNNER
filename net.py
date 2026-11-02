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
        try:
            data = sock.recv(1024)
            banner = data.decode('utf-8', errors='ignore').strip()
            if banner:
                print("[+] Port " + str(port) + " is open | Banner: " + banner)
            else:   
                print("[+] Port " + str(port) + " is open | No banner received")
        except:
            print(f"[+] Port {port} is open: Unable to detect version")
    except:
        pass

def scan(target,start,end):
    converted_ip = check_ip(target)
    print('\n' + '[# Scanning Target]---- ' + str(target))
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start, end + 1):
            executor.submit(scan_port, converted_ip, port)
        pass

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
