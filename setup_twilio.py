"""
Twilio Setup Helper Script
This script helps you set up your Twilio environment variables.
"""

import os
from pathlib import Path


def create_env_file():
    """Create a .env file with Twilio configuration template."""
    env_content = """# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# SendGrid Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=your_sendgrid_from_email_here
SENDGRID_FROM_NAME=AdsCompetitor

# Notification Settings
NOTIFICATION_ENABLED=true
NOTIFICATION_RETRY_ATTEMPTS=3
NOTIFICATION_TIMEOUT=30.0
"""
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite not in ['y', 'yes']:
            print("❌ Setup cancelled.")
            return False
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created .env file at {env_file.absolute()}")
        print("📝 Please edit the .env file and add your actual credentials.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def interactive_setup():
    """Interactive setup for Twilio credentials."""
    print("🔧 INTERACTIVE TWILIO SETUP")
    print("=" * 40)
    print()
    print("This will help you set up your Twilio credentials interactively.")
    print("You can get these from: https://console.twilio.com/")
    print()
    
    # Get Twilio credentials
    account_sid = input("Enter your Twilio Account SID: ").strip()
    auth_token = input("Enter your Twilio Auth Token: ").strip()
    phone_number = input("Enter your Twilio Phone Number (e.g., +1234567890): ").strip()
    
    if not all([account_sid, auth_token, phone_number]):
        print("❌ All fields are required!")
        return False
    
    # Validate phone number format
    if not phone_number.startswith('+'):
        print("⚠️  Phone number should start with '+' (e.g., +1234567890)")
        phone_number = input("Enter phone number again: ").strip()
        if not phone_number.startswith('+'):
            print("❌ Invalid phone number format!")
            return False
    
    # Create .env content
    env_content = f"""# Twilio SMS Configuration
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_PHONE_NUMBER={phone_number}

# SendGrid Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=your_sendgrid_from_email_here
SENDGRID_FROM_NAME=AdsCompetitor

# Notification Settings
NOTIFICATION_ENABLED=true
NOTIFICATION_RETRY_ATTEMPTS=3
NOTIFICATION_TIMEOUT=30.0
"""
    
    # Write to .env file
    env_file = Path(".env")
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ Created .env file with your Twilio credentials!")
        print(f"📁 Location: {env_file.absolute()}")
        print("\n🧪 You can now run: python test_twilio.py")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def show_twilio_guide():
    """Show Twilio setup guide."""
    print("📚 TWILIO SETUP GUIDE")
    print("=" * 50)
    print()
    print("1. 📝 Create a Twilio Account:")
    print("   - Go to: https://www.twilio.com/try-twilio")
    print("   - Sign up for a free account")
    print()
    print("2. 🔑 Get Your Credentials:")
    print("   - Go to: https://console.twilio.com/")
    print("   - Find your Account SID and Auth Token on the dashboard")
    print()
    print("3. 📱 Get a Phone Number:")
    print("   - Go to: Phone Numbers > Manage > Buy a number")
    print("   - Buy a phone number (free trial includes $15 credit)")
    print()
    print("4. 🔧 Set Up Environment Variables:")
    print("   - Run: python setup_twilio.py")
    print("   - Or manually create a .env file with your credentials")
    print()
    print("5. 🧪 Test Your Setup:")
    print("   - Run: python test_twilio.py")
    print()
    print("📞 Free Trial Limits:")
    print("   - $15 credit included")
    print("   - Can only send to verified phone numbers")
    print("   - Need to verify each recipient number in console")
    print()


def main():
    """Main setup function."""
    print("🔧 TWILIO SETUP HELPER")
    print("=" * 40)
    print()
    print("Choose an option:")
    print("1. Show setup guide")
    print("2. Create .env template file")
    print("3. Interactive setup")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            show_twilio_guide()
            break
        elif choice == "2":
            create_env_file()
            break
        elif choice == "3":
            interactive_setup()
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
