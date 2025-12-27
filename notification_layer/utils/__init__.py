"""
Utility functions for the Notification Layer.
"""

from .user_input import (
    collect_phone_numbers,
    collect_email_addresses,
    collect_user_contacts,
    display_user_summary,
    validate_phone_number,
    validate_email,
    normalize_phone_number
)

__all__ = [
    "collect_phone_numbers",
    "collect_email_addresses",
    "collect_user_contacts",
    "display_user_summary",
    "validate_phone_number",
    "validate_email",
    "normalize_phone_number"
]
