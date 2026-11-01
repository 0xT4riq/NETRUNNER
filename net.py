import socket
from IPy import IP
import time

def scan(target):
    converted_ip = check_ip(target)
    print('\n' + '[# Scanning Target]---- ' + str(target))
    for port in range(1, 65536):
        scan_port(converted_ip, port)


def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        print("[+] Port " + str(port) + " is open")
    except:
        pass

targets = input("[+] Enter target/s to scan (split multiple targets with ','): ")
if ',' in targets:
    for ip_add in targets.split(','):
        scan(ip_add.strip())
else:
    scan(targets)
