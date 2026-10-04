def alias_for(reseller_id: str) -> str:
    """Convert RS### to the required external-facing alias."""
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """Return False as soon as any raw reseller name appears verbatim."""
    return not any(name and name in text for name in reseller_names)
