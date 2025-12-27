"""
Demo script showing user input utilities in action.
This demonstrates the validation and collection functions without requiring manual input.
"""
import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.append(str(Path(__file__).parent))

from notification_layer.utils import (
    validate_phone_number,
    validate_email,
    normalize_phone_number,
    display_user_summary
)

print("=" * 60)
print("USER INPUT UTILITIES DEMO")
print("=" * 60)

# Demo 1: Phone Number Validation
print("\n1. PHONE NUMBER VALIDATION")
print("-" * 40)

test_phones = [
    ("+1234567890", True),
    ("+19876543210", True),
    ("1234567890", True),  # Will be normalized
    ("(123) 456-7890", True),
    ("invalid-phone", False),
    ("123", False),
    ("+44 20 1234 5678", True),
]

for phone, expected in test_phones:
    is_valid = validate_phone_number(phone)
    status = "[VALID]" if is_valid == expected else "[MISMATCH]"
    normalized = normalize_phone_number(phone) if is_valid else phone
    print(f"  {phone:20} -> {status:10} (Normalized: {normalized if is_valid else 'N/A'})")

# Demo 2: Email Validation
print("\n2. EMAIL VALIDATION")
print("-" * 40)

test_emails = [
    ("user@example.com", True),
    ("test.email+tag@example.co.uk", True),
    ("invalid-email", False),
    ("@example.com", False),
    ("user@", False),
    ("user.name@domain.com", True),
]

for email, expected in test_emails:
    is_valid = validate_email(email)
    status = "[VALID]" if is_valid == expected else "[MISMATCH]"
    print(f"  {email:30} -> {status}")

# Demo 3: User Summary Display
print("\n3. USER SUMMARY DISPLAY")
print("-" * 40)

sample_users = {
    "sms_users": [
        {"phone": "+1234567890", "name": "John Doe"},
        {"phone": "+1987654321", "name": "Jane Smith"},
        {"phone": "+1555123456", "name": "Bob Johnson"},
    ],
    "email_users": [
        {"email": "alice@example.com", "name": "Alice Brown"},
        {"email": "charlie@example.com", "name": "Charlie Wilson"},
        {"email": "diana@example.com", "name": "Diana Davis"},
    ]
}

display_user_summary(sample_users)

# Demo 4: Normalization Examples
print("\n4. PHONE NUMBER NORMALIZATION")
print("-" * 40)

normalization_examples = [
    "1234567890",
    "(123) 456-7890",
    "123-456-7890",
    "+1-234-567-8900",
    "123.456.7890",
]

print("  Format Variations -> E.164 Format:")
for phone in normalization_examples:
    try:
        if validate_phone_number(phone):
            normalized = normalize_phone_number(phone)
            print(f"  {phone:20} -> {normalized}")
        else:
            print(f"  {phone:20} -> INVALID (cannot normalize)")
    except Exception as e:
        print(f"  {phone:20} -> ERROR: {e}")

print("\n" + "=" * 60)
print("DEMO COMPLETE!")
print("=" * 60)
print("\nThe interactive scripts will prompt you to:")
print("  1. Enter phone numbers (one by one)")
print("  2. Enter email addresses (one by one)")
print("  3. Each will be validated automatically")
print("  4. You'll see a summary before sending")
print("\nTry running: python examples/interactive_send_ads.py")
