"""
Example usage of the Notification Layer for sending ads to user lists.

This example demonstrates how to:
1. Send individual SMS and email notifications
2. Send bulk notifications to user lists
3. Handle errors and success responses
4. Check provider status
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import the notification layer
sys.path.append(str(Path(__file__).parent.parent))

from notification_layer import NotificationLayer
from notification_layer.models.notification_types import NotificationType
from notification_layer.exceptions import NotificationError


def main():
    """Main example function."""
    print("AdsCompetitor Notification Layer Example")
    print("=" * 50)
    
    # Initialize the notification layer
    try:
        notification_layer = NotificationLayer()
        print("✓ Notification layer initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize notification layer: {e}")
        return
    
    # Check provider status
    print("\n1. Checking Provider Status")
    print("-" * 30)
    status = notification_layer.get_provider_status()
    print(f"Overall enabled: {status['overall_enabled']}")
    
    for provider_type, provider_info in status['providers'].items():
        print(f"{provider_type.upper()}:")
        print(f"  - Enabled: {provider_info['enabled']}")
        print(f"  - Provider: {provider_info['name']}")
        if 'balance' in provider_info:
            print(f"  - Balance: ${provider_info['balance']}")
    
    # Example 1: Send individual SMS
    print("\n2. Sending Individual SMS")
    print("-" * 30)
    try:
        result = notification_layer.send_sms(
            to_phone="+1234567890",  # Replace with actual phone number
            message="🚀 New ad campaign ready! Check out our latest offers at yourbusiness.com"
        )
        
        if result.success:
            print(f"✓ SMS sent successfully!")
            print(f"  - Message ID: {result.message_id}")
            print(f"  - Status: {result.status.value}")
            print(f"  - Delivery time: {result.delivery_time}")
        else:
            print(f"✗ SMS failed: {result.error_message}")
    except NotificationError as e:
        print(f"✗ SMS error: {e}")
    
    # Example 2: Send individual email
    print("\n3. Sending Individual Email")
    print("-" * 30)
    try:
        result = notification_layer.send_email(
            to_email="customer@example.com",  # Replace with actual email
            subject="🎯 Your Personalized Ad Campaign is Ready!",
            content="""
            Dear Customer,
            
            We've created a personalized ad campaign just for you!
            
            Campaign Highlights:
            • Targeted keywords: [Your keywords]
            • Local focus: [Your area]
            • Special offer: 20% off first month
            
            Click here to view: https://yourads.com/campaign/123
            
            Best regards,
            AdsCompetitor Team
            """,
            html_content="""
            <html>
            <body>
                <h2>🎯 Your Personalized Ad Campaign is Ready!</h2>
                <p>Dear Customer,</p>
                <p>We've created a personalized ad campaign just for you!</p>
                
                <h3>Campaign Highlights:</h3>
                <ul>
                    <li>Targeted keywords: <strong>[Your keywords]</strong></li>
                    <li>Local focus: <strong>[Your area]</strong></li>
                    <li>Special offer: <strong>20% off first month</strong></li>
                </ul>
                
                <p><a href="https://yourads.com/campaign/123" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Campaign</a></p>
                
                <p>Best regards,<br>AdsCompetitor Team</p>
            </body>
            </html>
            """
        )
        
        if result.success:
            print(f"✓ Email sent successfully!")
            print(f"  - Message ID: {result.message_id}")
            print(f"  - Status: {result.status.value}")
            print(f"  - Delivery time: {result.delivery_time}")
        else:
            print(f"✗ Email failed: {result.error_message}")
    except NotificationError as e:
        print(f"✗ Email error: {e}")
    
    # Example 3: Send to user list (SMS)
    print("\n4. Sending to User List (SMS)")
    print("-" * 30)
    
    # Sample user list with phone numbers
    user_list_sms = [
        {"phone": "+1234567890", "name": "John Doe", "location": "New York"},
        {"phone": "+1234567891", "name": "Jane Smith", "location": "Los Angeles"},
        {"phone": "+1234567892", "name": "Bob Johnson", "location": "Chicago"},
    ]
    
    sms_message = "🎉 New ad campaign launched! Get 20% off your first month. Reply STOP to opt out."
    
    try:
        results = notification_layer.send_to_user_list(
            user_list=user_list_sms,
            message_content=sms_message,
            notification_type=NotificationType.SMS
        )
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        print(f"📊 SMS Results: {successful} sent, {failed} failed")
        
        for i, result in enumerate(results):
            user = user_list_sms[i]
            status = "✓" if result.success else "✗"
            print(f"  {status} {user['name']} ({user['phone']}): {result.status.value}")
            if not result.success and result.error_message:
                print(f"    Error: {result.error_message}")
                
    except NotificationError as e:
        print(f"✗ Bulk SMS error: {e}")
    
    # Example 4: Send to user list (Email)
    print("\n5. Sending to User List (Email)")
    print("-" * 30)
    
    # Sample user list with email addresses
    user_list_email = [
        {"email": "customer1@example.com", "name": "Alice Brown", "company": "TechCorp"},
        {"email": "customer2@example.com", "name": "Charlie Wilson", "company": "StartupXYZ"},
        {"email": "customer3@example.com", "name": "Diana Davis", "company": "LocalBiz"},
    ]
    
    email_subject = "🚀 Your Custom Ad Campaign is Live!"
    email_content = """
    Dear {name},
    
    Great news! Your personalized ad campaign for {company} is now live and running.
    
    Campaign Performance:
    • Impressions: 1,250
    • Clicks: 45
    • Click-through rate: 3.6%
    • Cost per click: $0.85
    
    View detailed analytics: https://yourads.com/analytics/123
    
    Need help optimizing? Reply to this email or call us at (555) 123-4567.
    
    Best regards,
    Your AdsCompetitor Team
    """
    
    try:
        results = notification_layer.send_to_user_list(
            user_list=user_list_email,
            message_content=email_content,
            notification_type=NotificationType.EMAIL,
            subject=email_subject
        )
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        print(f"📊 Email Results: {successful} sent, {failed} failed")
        
        for i, result in enumerate(results):
            user = user_list_email[i]
            status = "✓" if result.success else "✗"
            print(f"  {status} {user['name']} ({user['email']}): {result.status.value}")
            if not result.success and result.error_message:
                print(f"    Error: {result.error_message}")
                
    except NotificationError as e:
        print(f"✗ Bulk email error: {e}")
    
    # Example 5: Error handling demonstration
    print("\n6. Error Handling Demonstration")
    print("-" * 30)
    
    # Try to send SMS with invalid phone number
    try:
        result = notification_layer.send_sms(
            to_phone="invalid-phone",
            message="This should fail"
        )
        print(f"Invalid phone result: {result.success} - {result.error_message}")
    except NotificationError as e:
        print(f"Invalid phone error: {e}")
    
    # Try to send email with invalid email
    try:
        result = notification_layer.send_email(
            to_email="invalid-email",
            subject="This should fail",
            content="Test content"
        )
        print(f"Invalid email result: {result.success} - {result.error_message}")
    except NotificationError as e:
        print(f"Invalid email error: {e}")
    
    # Close the notification layer
    notification_layer.close()
    print("\n✓ Notification layer closed successfully")


def demo_environment_setup():
    """Demonstrate environment variable setup."""
    print("\nEnvironment Variable Setup")
    print("=" * 50)
    print("To use the notification layer, set these environment variables:")
    print()
    print("# Twilio SMS Configuration")
    print("TWILIO_ACCOUNT_SID=your_twilio_account_sid_here")
    print("TWILIO_AUTH_TOKEN=your_twilio_auth_token_here")
    print("TWILIO_PHONE_NUMBER=your_twilio_phone_number_here")
    print()
    print("# SendGrid Email Configuration")
    print("SENDGRID_API_KEY=your_sendgrid_api_key_here")
    print("SENDGRID_FROM_EMAIL=your_sendgrid_from_email_here")
    print("SENDGRID_FROM_NAME=AdsCompetitor")
    print()
    print("# Optional Settings")
    print("NOTIFICATION_ENABLED=true")
    print("NOTIFICATION_RETRY_ATTEMPTS=3")
    print("NOTIFICATION_TIMEOUT=30.0")
    print()
    print("Or create a .env file with these variables (see env.example)")


if __name__ == "__main__":
    # Show environment setup info
    demo_environment_setup()
    
    # Run the main example
    main()
