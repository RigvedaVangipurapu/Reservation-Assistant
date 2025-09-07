#!/usr/bin/env python3
"""
Test the fixed date navigation
"""

from badminton_agent import BookingAgent
import time
from datetime import datetime, timedelta

def test_fixed_date_navigation():
    """Test the updated date navigation"""
    
    print("🧪 TESTING FIXED DATE NAVIGATION")
    print("=" * 50)
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded")
            
            # Check current state
            print("\n📅 STEP 1: Check current date...")
            page_text = agent.page.inner_text("body")
            import re
            
            current_date_match = re.search(r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),\s+([A-Z]+)\s+(\d+),\s+(\d{4})', page_text)
            if current_date_match:
                current_display = current_date_match.group(0)
                print(f"Current date display: {current_display}")
            
            current_url = agent.page.url
            print(f"Current URL: {current_url}")
            
            # Test date change to tomorrow
            print("\n🔄 STEP 2: Change to tomorrow...")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"Target date: {tomorrow}")
            
            result = agent.change_date(target_date=tomorrow)
            
            print(f"Change result: {result}")
            
            # Check if it worked
            time.sleep(2)
            
            new_url = agent.page.url
            new_page_text = agent.page.inner_text("body")
            
            new_date_match = re.search(r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),\s+([A-Z]+)\s+(\d+),\s+(\d{4})', new_page_text)
            if new_date_match:
                new_display = new_date_match.group(0)
                print(f"New date display: {new_display}")
            
            print(f"New URL: {new_url}")
            
            # Verify success
            if f"viewdate={tomorrow}" in new_url:
                print("✅ URL contains correct date parameter")
            else:
                print("❌ URL doesn't contain expected date parameter")
            
            if new_date_match and current_date_match:
                if new_display != current_display:
                    print(f"✅ Date display changed from '{current_display}' to '{new_display}'")
                else:
                    print(f"❌ Date display unchanged: '{new_display}'")
            
            # Test availability after date change
            print("\n📊 STEP 3: Test availability after date change...")
            slots_result = agent.get_available_slots()
            
            print(f"Slots found: {slots_result.get('total_slots', 0)}")
            print(f"Available: {slots_result.get('available_slots', 0)}")
            print(f"Date agent thinks: {slots_result.get('date', 'Unknown')}")
            
            if slots_result.get("slots"):
                print("Sample slots:")
                for i, slot in enumerate(slots_result["slots"][:3], 1):
                    print(f"  {i}. {slot.get('court', 'Unknown')} - {slot.get('time', 'Unknown')}")
            
            print(f"\n👀 Browser will stay open for 15 seconds for verification...")
            print(f"Please verify:")
            print(f"  • Does the date display match {tomorrow}?")
            print(f"  • Do the time slots look correct for tomorrow?")
            print(f"  • Are there booking elements visible?")
            
            time.sleep(15)
            
        else:
            print(f"❌ Failed to load page: {nav_result}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
    
    print(f"\n📝 Summary:")
    print(f"The fixed date navigation uses URL parameter: ?viewdate=YYYY-MM-DD")
    print(f"This should work reliably for changing dates on the Skedda website.")

if __name__ == "__main__":
    test_fixed_date_navigation()
