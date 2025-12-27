"""
Interactive script to collect user emails and phone numbers,
generate ads, and send them automatically.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from ai_generation_layer import AIGenerationLayer
from notification_layer import NotificationLayer
from notification_layer.models.notification_types import NotificationType
from notification_layer.exceptions import NotificationError
from notification_layer.utils import collect_user_contacts, display_user_summary


def main():
    """Main interactive function."""
    print("=" * 60)
    print("🎯 AdsCompetitor: Interactive Ad Generation & Sending")
    print("=" * 60)
    print()
    print("This script will:")
    print("1. Ask you to enter competitor information")
    print("2. Collect user phone numbers and emails")
    print("3. Generate ads using AI")
    print("4. Send ads to all users automatically")
    print()
    
    # Initialize layers
    print("Initializing system...")
    try:
        ai_layer = AIGenerationLayer()
        notification_layer = NotificationLayer()
        print("✓ System initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        print("Please check your environment variables and API keys.")
        return
    
    # Step 1: Get competitor information
    print("📝 STEP 1: Competitor Information")
    print("-" * 40)
    competitor_name = input("Enter competitor name (e.g., 'Local Pizza Palace'): ").strip()
    ad_copy = input("Enter competitor ad copy (press Enter to skip): ").strip()
    location = input("Enter location (e.g., 'Downtown', press Enter to skip): ").strip()
    zipcode = input("Enter ZIP code (e.g., '12345'): ").strip()
    
    # Get hashtags
    hashtags_input = input("Enter hashtags (comma-separated, e.g., '#pizza,#delivery'): ").strip()
    hashtags = [tag.strip() for tag in hashtags_input.split(',') if tag.strip()] if hashtags_input else []
    
    # Prepare competitor data
    competitor_data = {
        "competitor_name": competitor_name or "Competitor",
        "ad_copy": ad_copy or "Best service in town!",
        "hashtags": hashtags or ["#business", "#local"],
        "location": location or "Local Area",
        "special_offers": []
    }
    
    print(f"\n✓ Competitor data collected:")
    print(f"  - Name: {competitor_data['competitor_name']}")
    print(f"  - Location: {competitor_data['location']}")
    print(f"  - ZIP: {zipcode}")
    print(f"  - Hashtags: {', '.join(hashtags) if hashtags else 'None'}")
    
    # Step 2: Collect user contacts
    print("\n" + "=" * 60)
    print("📝 STEP 2: Collect User Contacts")
    print("=" * 60)
    
    users = collect_user_contacts(include_sms=True, include_email=True)
    sms_users = users.get("sms_users", [])
    email_users = users.get("email_users", [])
    
    display_user_summary(users)
    
    if not sms_users and not email_users:
        print("\n❌ No users entered. Exiting...")
        return
    
    # Step 3: Generate ads
    print("\n" + "=" * 60)
    print("🤖 STEP 3: Generate Ads with AI")
    print("=" * 60)
    
    print("\nGenerating ads...")
    try:
        generated_ads = ai_layer.generate_ads(
            competitor_data=competitor_data,
            hashtags=hashtags if hashtags else ["#business"],
            zipcode=zipcode or "12345"
        )
        
        print(f"\n✓ Generated {len(generated_ads)} ad(s)\n")
        
        # Display generated ads
        for i, ad in enumerate(generated_ads, 1):
            print(f"  Ad {i}:")
            print(f"    📰 Headline: {ad.headline}")
            print(f"    📝 Text: {ad.ad_text}")
            print(f"    🏷️  Hashtags: {', '.join(ad.hashtags)}")
            print(f"    🎯 CTA: {ad.cta}")
            print()
            
    except Exception as e:
        print(f"❌ Failed to generate ads: {e}")
        return
    
    # Step 4: Send ads
    print("=" * 60)
    print("📤 STEP 4: Send Ads to Users")
    print("=" * 60)
    
    # Confirm before sending
    print(f"\n⚠️  Ready to send {len(generated_ads)} ad(s) to:")
    if sms_users:
        print(f"   📱 {len(sms_users)} phone number(s)")
    if email_users:
        print(f"   📧 {len(email_users)} email address(es)")
    
    confirm = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Cancelled by user.")
        return
    
    # Send SMS
    sms_results = []
    if sms_users:
        print(f"\n📱 Sending via SMS ({len(sms_users)} recipients)...")
        for i, ad in enumerate(generated_ads, 1):
            print(f"  Sending Ad {i}...")
            
            sms_message = f"🎯 {ad.headline}\n\n{ad.ad_text}\n\n{ad.cta}\n\nHashtags: {', '.join(ad.hashtags)}"
            
            try:
                results = notification_layer.send_to_user_list(
                    user_list=sms_users,
                    message_content=sms_message,
                    notification_type=NotificationType.SMS
                )
                sms_results.extend(results)
                
                successful = sum(1 for r in results if r.success)
                print(f"    ✓ {successful}/{len(results)} SMS messages sent successfully")
                
            except NotificationError as e:
                print(f"    ❌ SMS error: {e}")
    
    # Send Email
    email_results = []
    if email_users:
        print(f"\n📧 Sending via Email ({len(email_users)} recipients)...")
        for i, ad in enumerate(generated_ads, 1):
            print(f"  Sending Ad {i}...")
            
            email_subject = f"🎯 New Ad Campaign: {ad.headline}"
            email_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">🎯 New Ad Campaign</h2>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #e74c3c; margin-top: 0;">{ad.headline}</h3>
                        <p style="font-size: 16px;">{ad.ad_text}</p>
                        <p style="text-align: center; margin: 20px 0;">
                            <strong style="background: #3498db; color: white; padding: 12px 24px; border-radius: 5px; display: inline-block;">
                                {ad.cta}
                            </strong>
                        </p>
                        <p style="color: #7f8c8d; font-size: 14px;">
                            Hashtags: {', '.join(ad.hashtags)}
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            for user in email_users:
                try:
                    result = notification_layer.send_email(
                        to_email=user["email"],
                        subject=email_subject,
                        content=f"New Ad Campaign: {ad.headline}\n\n{ad.ad_text}\n\n{ad.cta}",
                        html_content=email_content
                    )
                    email_results.append(result)
                    
                except NotificationError as e:
                    print(f"    ❌ Email error for {user.get('name', 'user')}: {e}")
                    email_results.append(None)
        
        successful_emails = sum(1 for r in email_results if r and r.success)
        print(f"    ✓ {successful_emails}/{len(email_results)} emails sent successfully")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    total_sms_sent = sum(1 for r in sms_results if r.success)
    total_email_sent = sum(1 for r in email_results if r and r.success)
    
    print(f"\n✅ Campaign completed!")
    print(f"   📱 SMS: {total_sms_sent}/{len(sms_results)} sent" if sms_results else "   📱 SMS: N/A")
    print(f"   📧 Email: {total_email_sent}/{len(email_results)} sent" if email_results else "   📧 Email: N/A")
    print(f"   🎯 Total: {total_sms_sent + total_email_sent} notifications delivered")
    
    # Close
    notification_layer.close()
    print("\n✓ System closed successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
