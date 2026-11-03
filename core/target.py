# ==============================
# TARGET VALIDATION
# ==============================


import socket
import ipaddress


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
            raise ValueError(
                f"Invalid target or hostname: {target}"
            )
