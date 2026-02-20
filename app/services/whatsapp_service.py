import re
from urllib.parse import quote


def normalize_phone(phone: str) -> str:
    """
    Normalize a Ugandan phone number to international format (2567XXXXXXXX).
    Handles formats: 07XX, +2567XX, 2567XX, 7XX
    """
    # Strip everything except digits and leading +
    digits = re.sub(r"[^\d]", "", phone)

    # Local format: 07XXXXXXXX → 2567XXXXXXXX
    if digits.startswith("0") and len(digits) == 10:
        digits = "256" + digits[1:]

    # Already has country code without +: 2567XXXXXXXX
    elif digits.startswith("256") and len(digits) == 12:
        pass  # already correct

    # Short form: 7XXXXXXXX (9 digits, no leading 0)
    elif len(digits) == 9:
        digits = "256" + digits

    return digits


def build_whatsapp_link(phone: str, listing_title: str) -> str:
    """
    Build a wa.me deep-link for a given phone number and listing title.
    The pre-filled message makes it easy for renters to reach out.
    """
    normalized = normalize_phone(phone)
    message = quote(
        f"Hi, I saw your listing on QuickRent: '{listing_title}'. Is it still available?"
    )
    return f"https://wa.me/{normalized}?text={message}"


def is_valid_phone(phone: str) -> bool:
    """
    Basic validation — must be a recognizable Ugandan mobile number.
    """
    normalized = normalize_phone(phone)
    # Ugandan numbers: 256 + 9 digits = 12 digits total
    return len(normalized) == 12 and normalized.startswith("256")