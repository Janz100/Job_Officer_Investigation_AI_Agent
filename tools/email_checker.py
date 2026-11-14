
import re
import dns.resolver

FREE_EMAIL_PROVIDERS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "icloud.com"
}

RESERVED_EXAMPLE_DOMAINS = {
    "example.com",
    "example.net",
    "example.org"
}


def is_reserved_example_domain(domain: str) -> bool:
    """Identify domains reserved for examples and documentation."""

    domain = domain.strip().lower().rstrip(".")

    if domain == "example":
        return True

    if domain.endswith(".example"):
        return True

    for reserved_domain in RESERVED_EXAMPLE_DOMAINS:
        if (
            domain == reserved_domain
            or domain.endswith("." + reserved_domain)
        ):
            return True

    return False


def check_email(email: str) -> dict:
    """
    Check email format, domain DNS and mail server records.

    Reserved example domains are identified separately.
    DNS and MX records do not prove that an email sender
    is genuine or authorized to represent a company.
    """

    email = email.strip().lower()

    result = {
        "email": email,
        "valid_format": False,
        "domain": None,
        "free_email_provider": False,
        "domain_exists": False,
        "has_mx_record": False,
        "reserved_example_domain": False
    }

    # Check basic email format
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        result["error"] = "Invalid email format."
        return result

    domain = email.split("@", 1)[1]

    result["valid_format"] = True
    result["domain"] = domain

    result["free_email_provider"] = (
        domain in FREE_EMAIL_PROVIDERS
    )

    # Detect reserved example domains before DNS checks
    if is_reserved_example_domain(domain):
        result["reserved_example_domain"] = True
        result["domain_exists"] = None
        result["has_mx_record"] = None
        result["status"] = "Placeholder/example email domain"
        result["verification_note"] = (
            "This is a reserved example domain. "
            "It cannot establish the identity of a real employer "
            "or verify a genuine recruitment contact."
        )
        return result

    # Check whether the domain has DNS records
    try:
        dns.resolver.resolve(domain, "A")
        result["domain_exists"] = True

    except dns.resolver.NXDOMAIN:
        result["domain_exists"] = False

    except Exception as e:
        result["domain_check_error"] = str(e)

    # Check whether the domain has mail server records
    try:
        dns.resolver.resolve(domain, "MX")
        result["has_mx_record"] = True

    except dns.resolver.NXDOMAIN:
        result["has_mx_record"] = False

    except Exception as e:
        result["mx_check_error"] = str(e)

    return result
