#!/usr/bin/env python3
"""
Test that the Streamlit app has valid syntax and imports
"""

def test_app_syntax():
    """Test that the app can be imported without errors"""
    try:
        print("🧪 Testing app syntax and imports...")
        
        # Test importing required modules
        import streamlit as st
        print("✅ Streamlit import successful")
        
        import os
        from datetime import datetime, timedelta
        print("✅ Standard library imports successful")
        
        from badminton_agent import BookingAgent
        print("✅ BookingAgent import successful")
        
        from booking_engine import EnhancedBookingAgent, BookingStatus
        print("✅ BookingEngine imports successful")
        
        # Test that the app file can be parsed
        with open("app.py", "r") as f:
            app_code = f.read()
        
        compile(app_code, "app.py", "exec")
        print("✅ App.py syntax is valid")
        
        print("\n🎉 All tests passed! The app should work correctly now.")
        print("\n🌐 To test the app:")
        print("   1. Make sure Streamlit is running: streamlit run app.py")
        print("   2. Open: http://localhost:8501")
        print("   3. Try typing: 'Book me a court tomorrow at 7 PM'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_app_syntax()
