"""
Quick verification script for SendGrid setup.
Run this to ensure everything is working before sending real emails.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import ssl

# Handle SSL for Windows
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

# Load environment
load_dotenv(Path(__file__).parent / '.env')

print("=" * 70)
print("SendGrid Quick Verification")
print("=" * 70)

# Check 1: Environment variables
print("\n✓ Checking environment variables...")
checks = {
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
    "SENDGRID_FROM_EMAIL": os.getenv("SENDGRID_FROM_EMAIL"),
    "SENDGRID_FROM_NAME": os.getenv("SENDGRID_FROM_NAME", "AdsCompetitor")
}

all_set = True
for key, value in checks.items():
    if value:
        masked = value if len(value) < 20 else f"{value[:7]}...{value[-4:]}"
        print(f"  ✓ {key}: {masked}")
    else:
        print(f"  ✗ {key}: NOT SET")
        all_set = False

if not all_set:
    print("\n❌ Some variables are missing. Check your .env file.")
    exit(1)

# Check 2: Dependencies
print("\n✓ Checking dependencies...")
try:
    import sendgrid
    print(f"  ✓ sendgrid library (v{sendgrid.__version__ if hasattr(sendgrid, '__version__') else 'installed'})")
except ImportError:
    print("  ✗ sendgrid library not installed")
    print("    Run: pip install sendgrid>=6.10.0")
    exit(1)

# Check 3: NotificationLayer
print("\n✓ Checking NotificationLayer...")
try:
    from notification_layer import NotificationLayer
    nl = NotificationLayer()
    status = nl.get_provider_status()
    
    if status['providers'].get('email', {}).get('enabled'):
        print("  ✓ Email provider is enabled and ready")
    else:
        print("  ✗ Email provider is not enabled")
        exit(1)
    
    nl.close()
except Exception as e:
    print(f"  ✗ Error: {e}")
    exit(1)

# All checks passed
print("\n" + "=" * 70)
print("✅ ALL CHECKS PASSED!")
print("=" * 70)
print("""
Your SendGrid integration is ready to use!

Next steps:
1. Verify your sender email at: https://app.sendgrid.com/settings/sender_auth
2. Run test: python test_sendgrid_simple.py
3. Check documentation: SENDGRID_SETUP_COMPLETE.md

Happy emailing! 📧
""")

