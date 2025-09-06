#!/usr/bin/env python3
"""
Test login functionality with credentials
"""

import getpass
from badminton_agent import BookingAgent

def test_login():
    """Test login with user credentials"""
    
    print("🔐 Testing Skedda Login")
    print("=" * 40)
    
    # Securely get credentials
    print("Please provide your Skedda credentials:")
    username = input("📧 Email/Username: ").strip()
    password = getpass.getpass("🔑 Password: ").strip()
    
    if not username or not password:
        print("❌ Both username and password are required")
        return
    
    print("\n🤖 Creating booking agent...")
    agent = BookingAgent(headless=False, slow_mo=1000)  # Visible mode to see login process
    
    try:
        print("\n🔐 Testing login...")
        login_result = agent.login_to_skedda(username, password)
        
        print(f"\n📊 Login Result:")
        print(f"   Success: {login_result['success']}")
        print(f"   Message: {login_result['message']}")
        
        if login_result["success"]:
            print("\n✅ Login successful! Now testing data access...")
            
            # Test getting availability with logged-in access
            print("\n📅 Testing availability access...")
            slots_result = agent.get_available_slots()
            
            print(f"   Slots found: {slots_result.get('total_slots', 0)}")
            print(f"   Available: {slots_result.get('available_slots', 0)}")
            
            if slots_result.get("slots"):
                print("\n📋 Sample slots with logged-in access:")
                for i, slot in enumerate(slots_result["slots"][:5]):
                    print(f"      {i+1}. {slot}")
            
            print("\n🔍 Page content check...")
            page_text_result = agent.get_page_text(max_length=500)
            if page_text_result["success"]:
                page_text = page_text_result["text"]
                if "VISITOR MODE" in page_text:
                    print("   ⚠️  Still in visitor mode - login may not have worked")
                else:
                    print("   ✅ Full access mode - login successful!")
            
        else:
            print(f"\n❌ Login failed:")
            print(f"   Error: {login_result.get('error', 'Unknown error')}")
            if login_result.get("page_content_sample"):
                print(f"   Page sample: {login_result['page_content_sample']}")
        
        print("\n⏰ Browser will stay open for 15 seconds for manual verification...")
        import time
        time.sleep(15)
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        
    finally:
        agent.stop_browser()
        
    print("\n💡 Next steps:")
    if login_result.get("success"):
        print("   ✅ Login works! The app will now show real availability data.")
        print("   ✅ You can now make actual bookings through the app.")
    else:
        print("   ❌ Login needs debugging. Check credentials and website structure.")

if __name__ == "__main__":
    test_login()
