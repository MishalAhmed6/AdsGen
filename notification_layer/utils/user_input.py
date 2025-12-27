"""
Utility functions for interactive user input collection.
"""

import re
from typing import List, Dict, Optional


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format (E.164 format preferred).
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove spaces and dashes
    cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Check E.164 format: + followed by 1-15 digits
    e164_pattern = r'^\+?[1-9]\d{1,14}$'
    
    if re.match(e164_pattern, cleaned):
        return True
    
    # Also accept US format: (123) 456-7890 or 123-456-7890
    us_pattern = r'^(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
    if re.match(us_pattern, phone):
        return True
    
    return False


def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number to E.164 format if possible.
    
    Args:
        phone: Phone number to normalize
        
    Returns:
        Normalized phone number
    """
    # Remove spaces, dashes, parentheses
    cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # If starts with 1 but no +, add +
    if cleaned.startswith('1') and not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    # If doesn't start with +, try to add it
    if not cleaned.startswith('+'):
        # Assume US number if 10 digits
        if len(cleaned) == 10:
            cleaned = '+1' + cleaned
        else:
            cleaned = '+' + cleaned
    
    return cleaned


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def collect_phone_numbers() -> List[Dict[str, str]]:
    """
    Interactively collect phone numbers from user.
    
    Returns:
        List of user dictionaries with phone numbers
    """
    users = []
    print("\n📱 PHONE NUMBER INPUT")
    print("=" * 50)
    print("Enter phone numbers to send SMS notifications.")
    print("Format: +1234567890 (with country code) or 1234567890")
    print("Press Enter with empty input to finish.\n")
    
    while True:
        name = input("Enter name (optional, press Enter to skip): ").strip()
        phone = input("Enter phone number (or press Enter to finish): ").strip()
        
        if not phone:
            break
        
        # Validate phone number
        if not validate_phone_number(phone):
            print(f"⚠️  Invalid phone number format: {phone}")
            retry = input("Do you want to try again? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                continue
            phone = input("Enter phone number again: ").strip()
            if not validate_phone_number(phone):
                print(f"❌ Skipping invalid phone number: {phone}")
                continue
        
        # Normalize phone number
        normalized_phone = normalize_phone_number(phone)
        
        user = {
            "phone": normalized_phone,
            "name": name or f"User {len(users) + 1}"
        }
        
        users.append(user)
        print(f"✓ Added: {user['name']} - {user['phone']}\n")
    
    print(f"\n✓ Collected {len(users)} phone number(s)")
    return users


def collect_email_addresses() -> List[Dict[str, str]]:
    """
    Interactively collect email addresses from user.
    
    Returns:
        List of user dictionaries with email addresses
    """
    users = []
    print("\n📧 EMAIL ADDRESS INPUT")
    print("=" * 50)
    print("Enter email addresses to send email notifications.")
    print("Format: user@example.com")
    print("Press Enter with empty input to finish.\n")
    
    while True:
        name = input("Enter name (optional, press Enter to skip): ").strip()
        email = input("Enter email address (or press Enter to finish): ").strip()
        
        if not email:
            break
        
        # Validate email
        if not validate_email(email):
            print(f"⚠️  Invalid email format: {email}")
            retry = input("Do you want to try again? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                continue
            email = input("Enter email address again: ").strip()
            if not validate_email(email):
                print(f"❌ Skipping invalid email: {email}")
                continue
        
        user = {
            "email": email.lower(),
            "name": name or f"User {len(users) + 1}"
        }
        
        users.append(user)
        print(f"✓ Added: {user['name']} - {user['email']}\n")
    
    print(f"\n✓ Collected {len(users)} email address(es)")
    return users


def collect_user_contacts(include_sms: bool = True, include_email: bool = True) -> Dict[str, List[Dict[str, str]]]:
    """
    Collect both phone numbers and email addresses interactively.
    
    Args:
        include_sms: Whether to collect SMS contacts
        include_email: Whether to collect email contacts
        
    Returns:
        Dictionary with 'sms_users' and 'email_users' lists
    """
    result = {
        "sms_users": [],
        "email_users": []
    }
    
    if include_sms:
        collect_sms = input("\nDo you want to send SMS notifications? (y/n): ").strip().lower()
        if collect_sms in ['y', 'yes']:
            result["sms_users"] = collect_phone_numbers()
    
    if include_email:
        collect_email = input("\nDo you want to send email notifications? (y/n): ").strip().lower()
        if collect_email in ['y', 'yes']:
            result["email_users"] = collect_email_addresses()
    
    return result


def display_user_summary(users: Dict[str, List[Dict[str, str]]]):
    """
    Display a summary of collected users.
    
    Args:
        users: Dictionary with 'sms_users' and 'email_users' lists
    """
    print("\n" + "=" * 50)
    print("📊 USER SUMMARY")
    print("=" * 50)
    
    if users.get("sms_users"):
        print(f"\n📱 SMS Recipients ({len(users['sms_users'])}):")
        for i, user in enumerate(users["sms_users"], 1):
            print(f"  {i}. {user.get('name', 'Unknown')} - {user['phone']}")
    else:
        print("\n📱 SMS Recipients: None")
    
    if users.get("email_users"):
        print(f"\n📧 Email Recipients ({len(users['email_users'])}):")
        for i, user in enumerate(users["email_users"], 1):
            print(f"  {i}. {user.get('name', 'Unknown')} - {user['email']}")
    else:
        print("\n📧 Email Recipients: None")
    
    total = len(users.get("sms_users", [])) + len(users.get("email_users", []))
    print(f"\n✓ Total recipients: {total}")
