
def validate_port_range(start, end):
    """
    Validate the supplied TCP port range.
    """

    if not (1 <= start <= 65535):
        raise ValueError(
            "Starting port must be between 1 and 65535."
        )

    if not (1 <= end <= 65535):
        raise ValueError(
            "Ending port must be between 1 and 65535."
        )

    if start > end:
        raise ValueError(
            "Starting port cannot be greater than ending port."
        )

def parse_ports(value):
    """
    Parse ports supplied as individual numbers or ranges.

    Examples:
        "80"              -> [80]
        "22,80,443"       -> [22, 80, 443]
        "1-1000"          -> [1, 2, ..., 1000]
        "22,80,8000-8100" -> [22, 80, 8000, ..., 8100]
    """
    ports = set()

    try:
        for part in value.split(","):
            part = part.strip()

            if not part:
                raise ValueError("Empty port entry.")

            if "-" in part:
                start, end = map(int, part.split("-"))

                validate_port_range(start, end)

                ports.update(range(start, end + 1))

            else:
                port = int(part)
                validate_port_range(port, port)
                ports.add(port)

    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid port specification: {error}")

    return sorted(ports)
