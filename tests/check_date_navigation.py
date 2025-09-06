#!/usr/bin/env python3
"""
Check what date the agent is looking at and verify date navigation works
"""

from badminton_agent import BookingAgent
import time
from datetime import datetime, timedelta

def check_date_navigation():
    """Check current date and test date navigation"""
    
    print("📅 DATE NAVIGATION CHECK")
    print("=" * 40)
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded")
            
            # Check what date is currently showing
            print("\n🔍 Step 1: What date is currently showing?")
            
            page = agent.page
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            # Look for date information on the page
            page_text = page.inner_text("body")
            
            # Extract date from page content
            import re
            date_patterns = [
                r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)[^,]*\d{4}',
                r'\d{1,2}/\d{1,2}/\d{4}',
                r'\d{4}-\d{2}-\d{2}',
                r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
            ]
            
            current_date_found = None
            for pattern in date_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    current_date_found = matches[0]
                    break
            
            print(f"📅 Date found on page: {current_date_found}")
            
            # Check URL for date parameter
            if "nbstart=" in current_url:
                url_date = current_url.split("nbstart=")[1].split("&")[0].split("T")[0]
                print(f"📅 Date in URL: {url_date}")
            
            print("\n👀 LOOK AT THE BROWSER - What date do you see displayed?")
            time.sleep(5)
            
            # Now let's try to change to tomorrow's date
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            
            print(f"\n🔄 Step 2: Trying to navigate to tomorrow ({tomorrow_str})...")
            print("Watch the browser - you should see the date change!")
            
            # Use the agent's change_date function
            date_result = agent.change_date(target_date=tomorrow_str)
            
            print(f"Date change result: {date_result}")
            
            # Wait and check what happened
            time.sleep(3)
            
            # Check if URL changed
            new_url = page.url
            print(f"New URL: {new_url}")
            
            # Check if page content changed
            new_page_text = page.inner_text("body")
            
            new_date_found = None
            for pattern in date_patterns:
                matches = re.findall(pattern, new_page_text, re.IGNORECASE)
                if matches:
                    new_date_found = matches[0]
                    break
            
            print(f"📅 New date found on page: {new_date_found}")
            
            # Check URL for new date parameter
            if "nbstart=" in new_url:
                new_url_date = new_url.split("nbstart=")[1].split("&")[0].split("T")[0]
                print(f"📅 New date in URL: {new_url_date}")
            
            print(f"\n📊 DATE CHANGE ANALYSIS:")
            print(f"   Requested date: {tomorrow_str}")
            print(f"   Before change: Page={current_date_found}, URL={current_url.split('nbstart=')[1].split('&')[0].split('T')[0] if 'nbstart=' in current_url else 'not found'}")
            print(f"   After change:  Page={new_date_found}, URL={new_url.split('nbstart=')[1].split('&')[0].split('T')[0] if 'nbstart=' in new_url else 'not found'}")
            
            if tomorrow_str in new_url:
                print("   ✅ URL successfully updated to tomorrow")
            else:
                print("   ❌ URL did not change to tomorrow")
            
            if new_date_found != current_date_found:
                print("   ✅ Page content shows date changed")
            else:
                print("   ❌ Page content still shows same date")
            
            print(f"\n👀 BROWSER CHECK:")
            print(f"   Look at the browser window now.")
            print(f"   • Did you see the date change in the browser?")
            print(f"   • What date is currently displayed?")
            print(f"   • Does it match tomorrow's date ({tomorrow.strftime('%A, %B %d, %Y')})?")
            
            # Now let's get slots for the current date and see what the agent thinks
            print(f"\n🔍 Step 3: Getting availability for what the agent thinks is the current date...")
            
            slots_result = agent.get_available_slots()
            
            print(f"Agent thinks current date is: {slots_result.get('date', 'Unknown')}")
            print(f"Agent found {slots_result.get('total_slots', 0)} slots")
            
            if slots_result.get("slots"):
                print(f"Sample slots (first 3):")
                for i, slot in enumerate(slots_result["slots"][:3], 1):
                    print(f"   {i}. {slot.get('court', 'Unknown')} - {slot.get('time', 'Unknown')}")
            
            print(f"\n⚠️  IMPORTANT QUESTION:")
            user_current_date = input(f"👤 What date do you ACTUALLY see in the browser right now? ")
            
            agent_date = slots_result.get('date', 'Unknown')
            url_date = new_url.split('nbstart=')[1].split('&')[0].split('T')[0] if 'nbstart=' in new_url else 'Unknown'
            
            print(f"\n📊 DATE MISMATCH ANALYSIS:")
            print(f"   You see: {user_current_date}")
            print(f"   Agent thinks: {agent_date}")
            print(f"   URL shows: {url_date}")
            print(f"   Requested: {tomorrow_str}")
            
            if user_current_date.lower() != tomorrow_str and user_current_date.lower() not in tomorrow.strftime('%A, %B %d, %Y').lower():
                print(f"\n❌ MAJOR ISSUE: Date navigation is not working!")
                print(f"   The agent thinks it changed the date but the browser still shows a different date.")
                print(f"   This explains why availability data doesn't match what you see.")
            else:
                print(f"\n✅ Date navigation appears to be working correctly.")
            
            print(f"\n⏰ Browser staying open for 20 seconds for observation...")
            time.sleep(20)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    check_date_navigation()
