import socket
import ipaddress
import time
import threading



def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ipaddress, port))
        print("[+] Port " + str(port) + " is open")
        sock.close()
    except:
        pass

def scan(target,start,end):
    converted_ip = check_ip(target)
    print('\n' + '[# Scanning Target]---- ' + str(target))
    for port in range(start, end + 1):
        thread = threading.Thread(target=scan_port, args=(converted_ip, port))
        thread.start()

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
