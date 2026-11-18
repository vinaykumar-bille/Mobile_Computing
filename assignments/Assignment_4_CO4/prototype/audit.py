"""Reasoned configuration checks, NOT live Android security verification."""


def audit(config):
    checks = {
        "https": config.get("https_only") is True,
        "private_token": config.get("private_token_storage") is True,
        "signed_updates": config.get("signed_updates") is True,
        "least_privilege": config.get("permission_on_demand") is True,
        "components": config.get("internal_components_exported") is False,
    }
    return checks


def verdict(checks):
    return "PASS (design flags only)" if all(checks.values()) else "REVIEW REQUIRED"
