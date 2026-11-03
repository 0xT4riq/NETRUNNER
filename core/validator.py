
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
