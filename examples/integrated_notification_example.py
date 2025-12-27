"""
Integrated example showing how to use the Notification Layer with the AI Generation Layer
to automatically send generated ads to user lists.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import the layers
sys.path.append(str(Path(__file__).parent.parent))

from ai_generation_layer import AIGenerationLayer
from notification_layer import NotificationLayer
from notification_layer.models.notification_types import NotificationType
from notification_layer.exceptions import NotificationError
from notification_layer.utils import collect_user_contacts, display_user_summary


def generate_and_send_ads():
    """Generate ads using AI and send them to user lists."""
    print("AdsCompetitor: Generate and Send Ads Example")
    print("=" * 60)
    
    # Initialize both layers
    try:
        print("Initializing AI Generation Layer...")
        ai_layer = AIGenerationLayer()
        print("✓ AI Generation Layer initialized")
        
        print("Initializing Notification Layer...")
        notification_layer = NotificationLayer()
        print("✓ Notification Layer initialized")
    except Exception as e:
        print(f"✗ Failed to initialize layers: {e}")
        return
    
    # Sample competitor data
    competitor_data = {
        "competitor_name": "Local Pizza Palace",
        "ad_copy": "Best pizza in town! Fresh ingredients, fast delivery. Order now for 20% off!",
        "hashtags": ["#pizza", "#delivery", "#local", "#fresh"],
        "location": "Downtown",
        "special_offers": ["20% off first order", "Free delivery over $25"]
    }
    
    # Collect user contacts interactively
    print("\n📝 COLLECT USER CONTACTS")
    print("=" * 60)
    print("You'll be asked to enter phone numbers and email addresses")
    print("to send the generated ads to.")
    print()
    
    users = collect_user_contacts(include_sms=True, include_email=True)
    sms_users = users.get("sms_users", [])
    email_users = users.get("email_users", [])
    
    # Display summary
    display_user_summary(users)
    
    # Check if we have any users
    if not sms_users and not email_users:
        print("\n❌ No users entered. Exiting...")
        return
    
    # Step 1: Generate ads using AI
    print("\n1. Generating Ads with AI")
    print("-" * 30)
    
    try:
        generated_ads = ai_layer.generate_ads(
            competitor_data=competitor_data,
            hashtags=competitor_data["hashtags"],
            zipcode="12345"
        )
        
        print(f"✓ Generated {len(generated_ads)} ads")
        
        # Display generated ads
        for i, ad in enumerate(generated_ads, 1):
            print(f"\n  Ad {i}:")
            print(f"    Headline: {ad.headline}")
            print(f"    Text: {ad.ad_text}")
            print(f"    Hashtags: {', '.join(ad.hashtags)}")
            print(f"    CTA: {ad.cta}")
            
    except Exception as e:
        print(f"✗ Failed to generate ads: {e}")
        return
    
    # Step 2: Send ads via SMS
    sms_results = []
    if sms_users:
        print(f"\n2. Sending Ads via SMS ({len(sms_users)} recipients)")
        print("-" * 40)
        
        for i, ad in enumerate(generated_ads, 1):
            print(f"\n  Sending Ad {i} via SMS...")
            
            # Create SMS-friendly message
            sms_message = f"🎯 {ad.headline}\n\n{ad.ad_text}\n\n{ad.cta}\n\nHashtags: {', '.join(ad.hashtags)}"
            
            try:
                results = notification_layer.send_to_user_list(
                    user_list=sms_users,
                    message_content=sms_message,
                    notification_type=NotificationType.SMS
                )
                
                sms_results.extend(results)
                
                # Count results
                successful = sum(1 for r in results if r.success)
                failed = len(results) - successful
                
                print(f"    ✓ Sent to {successful} users, {failed} failed")
                
                # Show failed results
                for j, result in enumerate(results):
                    if not result.success:
                        user = sms_users[j]
                        print(f"    ✗ {user['name']}: {result.error_message}")
                        
            except NotificationError as e:
                print(f"    ✗ SMS sending failed: {e}")
    else:
        print(f"\n2. Skipping SMS (no phone numbers provided)")
    
    # Step 3: Send ads via Email
    email_results = []
    if email_users:
        print(f"\n3. Sending Ads via Email ({len(email_users)} recipients)")
        print("-" * 42)
        
        for i, ad in enumerate(generated_ads, 1):
            print(f"\n  Sending Ad {i} via Email...")
            
            # Create email content
            email_subject = f"🎯 New Ad Campaign: {ad.headline}"
            
            # Personalize email content for each user
            for user in email_users:
                email_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">🎯 New Ad Campaign</h2>
                    
                    <p>Dear {user.get('name', 'Customer')},</p>
                    
                    <p>We've created a personalized ad campaign just for you!</p>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #e74c3c; margin-top: 0;">{ad.headline}</h3>
                        <p style="font-size: 16px;">{ad.ad_text}</p>
                        <p style="text-align: center; margin: 20px 0;">
                            <a href="https://yourads.com/campaign/{ad.headline.lower().replace(' ', '-')}" 
                               style="background: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                {ad.cta}
                            </a>
                        </p>
                        <p style="color: #7f8c8d; font-size: 14px;">
                            Hashtags: {', '.join(ad.hashtags)}
                        </p>
                    </div>
                    
                    <p><strong>Why this ad works:</strong></p>
                    <ul>
                        <li>Local focus targeting {user['location']} area</li>
                        <li>Compelling headline that grabs attention</li>
                        <li>Clear call-to-action for immediate response</li>
                        <li>Relevant hashtags for social media reach</li>
                    </ul>
                    
                    <p>Want to customize this campaign? Reply to this email or call us at (555) 123-4567.</p>
                    
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 30px 0;">
                    <p style="font-size: 12px; color: #95a5a6;">
                        AdsCompetitor Team<br>
                        <a href="mailto:support@adscompetitor.com">support@adscompetitor.com</a><br>
                        <a href="https://adscompetitor.com">www.adscompetitor.com</a>
                    </p>
                </div>
            </body>
            </html>
            """
            
            try:
                result = notification_layer.send_email(
                    to_email=user["email"],
                    subject=email_subject,
                    content=f"New Ad Campaign: {ad.headline}\n\n{ad.ad_text}\n\n{ad.cta}",
                    html_content=email_content
                )
                
                email_results.append(result)
                
                if result.success:
                    print(f"    ✓ Sent to {user['name']} ({user['email']})")
                else:
                    print(f"    ✗ Failed to send to {user['name']}: {result.error_message}")
                    
            except NotificationError as e:
                print(f"    ✗ Email failed for {user['name']}: {e}")
                email_results.append(None)
    else:
        print(f"\n3. Skipping Email (no email addresses provided)")
    
    # Step 4: Summary Report
    print(f"\n4. Campaign Summary Report")
    print("-" * 30)
    
    # SMS Summary
    total_sms_attempts = len(sms_results)
    successful_sms = sum(1 for r in sms_results if r.success)
    failed_sms = total_sms_attempts - successful_sms
    
    print(f"\n📱 SMS Campaign:")
    print(f"  - Total attempts: {total_sms_attempts}")
    print(f"  - Successful: {successful_sms}")
    print(f"  - Failed: {failed_sms}")
    print(f"  - Success rate: {(successful_sms/total_sms_attempts*100):.1f}%" if total_sms_attempts > 0 else "  - Success rate: 0%")
    
    # Email Summary
    total_email_attempts = len(email_results)
    successful_emails = sum(1 for r in email_results if r and r.success)
    failed_emails = total_email_attempts - successful_emails
    
    print(f"\n📧 Email Campaign:")
    print(f"  - Total attempts: {total_email_attempts}")
    print(f"  - Successful: {successful_emails}")
    print(f"  - Failed: {failed_emails}")
    print(f"  - Success rate: {(successful_emails/total_email_attempts*100):.1f}%" if total_email_attempts > 0 else "  - Success rate: 0%")
    
    # Overall Summary
    total_attempts = total_sms_attempts + total_email_attempts
    total_successful = successful_sms + successful_emails
    total_failed = failed_sms + failed_emails
    
    print(f"\n🎯 Overall Campaign:")
    print(f"  - Total notifications sent: {total_attempts}")
    print(f"  - Successful deliveries: {total_successful}")
    print(f"  - Failed deliveries: {total_failed}")
    print(f"  - Overall success rate: {(total_successful/total_attempts*100):.1f}%" if total_attempts > 0 else "  - Overall success rate: 0%")
    
    # Step 5: Provider Status Check
    print(f"\n5. Provider Status Check")
    print("-" * 25)
    
    status = notification_layer.get_provider_status()
    print(f"Overall notifications enabled: {status['overall_enabled']}")
    
    for provider_type, provider_info in status['providers'].items():
        print(f"\n{provider_type.upper()} Provider:")
        print(f"  - Enabled: {provider_info['enabled']}")
        print(f"  - Provider: {provider_info['name']}")
        if 'balance' in provider_info and provider_info['balance'] is not None:
            print(f"  - Account balance: ${provider_info['balance']:.2f}")
    
    # Close layers
    notification_layer.close()
    print(f"\n✓ Campaign completed successfully!")
    print(f"✓ All layers closed cleanly")


def demo_user_list_management():
    """Demonstrate advanced user list management."""
    print("\n" + "=" * 60)
    print("Advanced User List Management Demo")
    print("=" * 60)
    
    # Sample comprehensive user database
    user_database = [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@restaurant.com",
            "phone": "+1234567890",
            "business": "Downtown Bistro",
            "business_type": "restaurant",
            "location": "Downtown",
            "preferred_contact": "email",
            "subscription_status": "active",
            "last_contact": "2023-01-15"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@retail.com",
            "phone": "+1234567891",
            "business": "Fashion Forward",
            "business_type": "retail",
            "location": "Mall District",
            "preferred_contact": "sms",
            "subscription_status": "active",
            "last_contact": "2023-01-10"
        },
        {
            "id": 3,
            "name": "Bob Johnson",
            "email": "bob@service.com",
            "phone": "+1234567892",
            "business": "Quick Clean",
            "business_type": "service",
            "location": "University Area",
            "preferred_contact": "email",
            "subscription_status": "inactive",
            "last_contact": "2022-12-20"
        },
        {
            "id": 4,
            "name": "Alice Brown",
            "email": "alice@beauty.com",
            "phone": "+1234567893",
            "business": "Beauty Studio",
            "business_type": "beauty",
            "location": "Main Street",
            "preferred_contact": "sms",
            "subscription_status": "active",
            "last_contact": "2023-01-20"
        }
    ]
    
    # Filter users based on criteria
    def filter_users(users, criteria):
        """Filter users based on given criteria."""
        filtered = users.copy()
        
        for key, value in criteria.items():
            if key == "business_type":
                filtered = [u for u in filtered if u.get("business_type") == value]
            elif key == "location":
                filtered = [u for u in filtered if u.get("location") == value]
            elif key == "preferred_contact":
                filtered = [u for u in filtered if u.get("preferred_contact") == value]
            elif key == "subscription_status":
                filtered = [u for u in filtered if u.get("subscription_status") == value]
        
        return filtered
    
    # Example filtering scenarios
    print("\n1. Restaurant owners in Downtown area:")
    restaurant_users = filter_users(user_database, {"business_type": "restaurant", "location": "Downtown"})
    for user in restaurant_users:
        print(f"  - {user['name']} ({user['business']}) - {user['preferred_contact']}")
    
    print("\n2. Active subscribers who prefer SMS:")
    sms_users = filter_users(user_database, {"subscription_status": "active", "preferred_contact": "sms"})
    for user in sms_users:
        print(f"  - {user['name']} ({user['business']}) - {user['phone']}")
    
    print("\n3. All users by contact preference:")
    email_users = filter_users(user_database, {"preferred_contact": "email"})
    print(f"  Email users: {len(email_users)}")
    for user in email_users:
        print(f"    - {user['name']} ({user['email']})")
    
    sms_preferred = filter_users(user_database, {"preferred_contact": "sms"})
    print(f"  SMS users: {len(sms_preferred)}")
    for user in sms_preferred:
        print(f"    - {user['name']} ({user['phone']})")


if __name__ == "__main__":
    # Run the main example
    generate_and_send_ads()
    
    # Run the advanced user management demo
    demo_user_list_management()
