
import socket

from config import BANNER_TIMEOUT, HTTP_PORTS


def grab_banner(sock, hostname, port):
    """
    Collect a service banner or protocol response.

    HTTP services receive a HEAD request.
    Other services are checked for automatic banners.
    """

    sock.settimeout(BANNER_TIMEOUT)

    try:
        if port in HTTP_PORTS:

            request = (
                f"HEAD / HTTP/1.1\r\n"
                f"Host: {hostname}\r\n"
                f"Connection: close\r\n\r\n"
            )

            sock.sendall(request.encode("ascii"))

        data = sock.recv(1024)

        return data.decode(
            "utf-8",
            errors="ignore"
        ).strip()

    except (socket.timeout, OSError):
        return ""


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
    Identify a service using its response banner.
    """

    if not banner:
        return "Unknown"

    upper_banner = banner.upper()

    if upper_banner.startswith("SSH-"):
        return "SSH"

    elif upper_banner.startswith("HTTP/"):
        return "HTTP"

    elif upper_banner.startswith("220"):
        if "ESMTP" in upper_banner or "SMTP" in upper_banner:
            return "SMTP"

        return "FTP/SMTP (Possible)"

    elif upper_banner.startswith("+OK"):
        return "POP3"

    elif upper_banner.startswith("* OK"):
        return "IMAP"

    return "Unknown"
