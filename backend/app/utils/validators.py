import validators
import socket

def is_valid_domain(domain: str) -> bool:
    return validators.domain(domain) is True

def check_domain_exists(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False