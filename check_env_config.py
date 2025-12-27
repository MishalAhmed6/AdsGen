"""Check .env file configuration."""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Load .env if it exists
env_path = Path('.env')
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print("✓ .env file found and loaded\n")
    except ImportError:
        print("⚠ python-dotenv not installed, checking file directly\n")
    
    # Check required variables
    print("=" * 50)
    print("Environment Variables Check")
    print("=" * 50)
    
    # AI Generation
    print("\n🤖 AI Generation (Gemini):")
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        print(f"  ✓ GEMINI_API_KEY: CONFIGURED ({len(gemini_key)} chars)")
    else:
        print("  ✗ GEMINI_API_KEY: NOT CONFIGURED")
    
    # Twilio (SMS)
    print("\n📱 Twilio (SMS):")
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN', '')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    if twilio_sid and twilio_sid != 'your_twilio_account_sid_here':
        print(f"  ✓ TWILIO_ACCOUNT_SID: CONFIGURED ({len(twilio_sid)} chars)")
    else:
        print("  ✗ TWILIO_ACCOUNT_SID: NOT CONFIGURED")
    
    if twilio_token and twilio_token != 'your_twilio_auth_token_here':
        print(f"  ✓ TWILIO_AUTH_TOKEN: CONFIGURED ({len(twilio_token)} chars)")
    else:
        print("  ✗ TWILIO_AUTH_TOKEN: NOT CONFIGURED")
    
    if twilio_phone and twilio_phone != 'your_twilio_phone_number_here':
        print(f"  ✓ TWILIO_PHONE_NUMBER: CONFIGURED ({twilio_phone})")
    else:
        print("  ✗ TWILIO_PHONE_NUMBER: NOT CONFIGURED")
    
    # SendGrid (Email)
    print("\n📧 SendGrid (Email):")
    sendgrid_key = os.getenv('SENDGRID_API_KEY', '')
    sendgrid_email = os.getenv('SENDGRID_FROM_EMAIL', '')
    
    if sendgrid_key and sendgrid_key != 'your_sendgrid_api_key_here':
        print(f"  ✓ SENDGRID_API_KEY: CONFIGURED ({len(sendgrid_key)} chars)")
    else:
        print("  ✗ SENDGRID_API_KEY: NOT CONFIGURED")
    
    if sendgrid_email and sendgrid_email != 'your_sendgrid_from_email_here':
        print(f"  ✓ SENDGRID_FROM_EMAIL: CONFIGURED ({sendgrid_email})")
    else:
        print("  ✗ SENDGRID_FROM_EMAIL: NOT CONFIGURED")
    
    # Notification settings
    print("\n⚙️  Notification Settings:")
    notif_enabled = os.getenv('NOTIFICATION_ENABLED', 'true')
    print(f"  NOTIFICATION_ENABLED: {notif_enabled}")
    
    print("\n" + "=" * 50)
    
    # Summary
    configured_count = sum([
        bool(gemini_key and gemini_key != 'your_gemini_api_key_here'),
        bool(twilio_sid and twilio_sid != 'your_twilio_account_sid_here'),
        bool(twilio_token and twilio_token != 'your_twilio_auth_token_here'),
        bool(twilio_phone and twilio_phone != 'your_twilio_phone_number_here'),
        bool(sendgrid_key and sendgrid_key != 'your_sendgrid_api_key_here'),
        bool(sendgrid_email and sendgrid_email != 'your_sendgrid_from_email_here')
    ])
    
    total_count = 6
    
    print(f"\nSummary: {configured_count}/{total_count} variables configured")
    
    if configured_count == total_count:
        print("✅ All required variables are configured!")
    elif configured_count > 0:
        print("⚠️  Some variables are missing. The app may not work fully.")
    else:
        print("❌ No variables configured. Please fill in your .env file.")
        
else:
    print("❌ .env file not found!")
    print(f"   Expected location: {env_path.absolute()}")
    print("\n   Please create .env file by copying env.example:")
    print("   Copy-Item env.example .env")

