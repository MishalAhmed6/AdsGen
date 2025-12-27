#!/usr/bin/env python3
"""
Test script to verify Gemini API key independently.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded .env file from: {env_path}")
else:
    print("⚠ .env file not found")

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

print(f"\nAPI Key found: {api_key[:15]}...{api_key[-10:]}")
print(f"Key length: {len(api_key)} characters")
print(f"Key contains spaces: {api_key != api_key.strip()}")
print()

# Test with google.generativeai
try:
    import google.generativeai as genai
    print("Testing with google.generativeai...")
    print("-" * 50)
    
    # Configure
    genai.configure(api_key=api_key)
    print("✓ Configuration successful")
    
    # List models
    print("\nAttempting to list available models...")
    try:
        models = genai.list_models()
        print(f"✓ Successfully connected! Found {len(list(models))} models")
    except Exception as e:
        print(f"⚠ Could not list models: {str(e)[:200]}")
    
    # Test generation
    print("\nAttempting to generate content...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content('Say "Hello" in one word only.')
    
    print(f"✓ API KEY IS VALID!")
    print(f"✓ Generated response: {response.text}")
    print("\n" + "=" * 50)
    print("✅ SUCCESS: Your API key is working correctly!")
    print("=" * 50)
    
except ImportError:
    print("❌ google-generativeai package not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)
except Exception as e:
    error_str = str(e)
    print(f"❌ API KEY TEST FAILED")
    print(f"Error: {error_str[:500]}")
    print("\n" + "=" * 50)
    print("❌ FAILED: API key is invalid or has issues")
    print("=" * 50)
    
    # Provide helpful suggestions
    if "API key not valid" in error_str or "API_KEY_INVALID" in error_str:
        print("\n💡 Suggestions:")
        print("1. Get a new API key from: https://aistudio.google.com/app/apikey")
        print("2. Make sure the API key doesn't have extra spaces or quotes")
        print("3. Verify the key is active in Google AI Studio")
        print("4. Check if there are any API restrictions on the key")
    
    sys.exit(1)

