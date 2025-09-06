#!/usr/bin/env python3
"""
Check the status of our Badminton Booking App
"""

import requests
import subprocess
import time

def check_app_status():
    """Check if the Streamlit app is running and accessible"""
    
    print("🔍 Checking Badminton Booking App Status...")
    
    # Check if Streamlit process is running
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'streamlit run app.py' in result.stdout:
            print("✅ Streamlit process is running")
        else:
            print("❌ Streamlit process not found")
            return False
    except Exception as e:
        print(f"❌ Error checking process: {e}")
        return False
    
    # Check if the web server is responding
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        if response.status_code == 200:
            print("✅ Web server is responding")
            print("🌐 App is accessible at: http://localhost:8501")
        else:
            print(f"⚠️ Web server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web server")
        print("⏳ The app might still be starting up. Wait a moment and try again.")
        return False
    except Exception as e:
        print(f"❌ Error checking web server: {e}")
        return False
    
    print("\n🎉 App Status: RUNNING")
    print("\n📱 How to use:")
    print("   1. Open your browser")
    print("   2. Go to: http://localhost:8501")
    print("   3. Type: 'Book me a court tomorrow at 7 PM'")
    print("   4. Follow the prompts!")
    
    print("\n✨ Features available:")
    print("   ✅ Natural language booking requests")
    print("   ✅ Smart time and court matching")
    print("   ✅ Alternative suggestions")
    print("   ✅ User-friendly confirmation flow")
    print("   ✅ Clean chat interface")
    
    return True

if __name__ == "__main__":
    check_app_status()
