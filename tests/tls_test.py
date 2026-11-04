from detection.tls import inspect_tls

result = inspect_tls("google.com")

for key, value in result.items():
    print(f"{key}: {value}")