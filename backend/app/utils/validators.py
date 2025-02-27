import validators

def is_valid_domain(domain: str) -> bool:
    return validators.domain(domain) is True
