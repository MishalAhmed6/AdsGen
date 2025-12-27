"""
Start the web application on port 5001.
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Change to web_app directory
os.chdir(Path(__file__).parent / 'web_app')

# Import and run the app
from app import app

if __name__ == '__main__':
    port = 5001
    print("=" * 60)
    print("AdsCompetitor Web Application")
    print("=" * 60)
    print(f"\nStarting server on port {port}...")
    print(f"Open your browser to: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=port)
