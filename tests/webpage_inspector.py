#!/usr/bin/env python3
"""
Comprehensive webpage inspector to understand the Skedda booking structure
"""

from badminton_agent import BookingAgent
import time

def inspect_webpage_structure():
    """Interactive webpage inspector with detailed questions"""
    
    print("🔍 COMPREHENSIVE WEBPAGE INSPECTOR")
    print("=" * 50)
    print("Let's understand your webpage structure step by step")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            page = agent.page
            
            print("✅ Page loaded successfully")
            print("\n👀 Please look at the browser window and answer these detailed questions:")
            
            # SECTION 1: BASIC PAGE LAYOUT
            print("\n" + "="*60)
            print("SECTION 1: BASIC PAGE LAYOUT")
            print("="*60)
            
            layout_type = input("1. What type of layout do you see?\n   a) Calendar grid view\n   b) Day schedule view (vertical timeline)\n   c) List view\n   d) Other\n   Your answer: ").strip()
            
            date_display = input("\n2. Where is the current date displayed?\n   a) Top left corner\n   b) Top center\n   c) Top right corner\n   d) In a header bar\n   e) Other location\n   Your answer: ").strip()
            
            current_date_text = input("\n3. What exactly does the date text say? (copy exactly): ").strip()
            
            # SECTION 2: COURT LAYOUT
            print("\n" + "="*60)
            print("SECTION 2: COURT LAYOUT")
            print("="*60)
            
            court_layout = input("4. How are courts displayed?\n   a) Horizontal columns (Court 1, Court 2, etc. across the top)\n   b) Vertical rows (Court 1, Court 2, etc. down the side)\n   c) In a dropdown/selector\n   d) Other\n   Your answer: ").strip()
            
            court_names = input("\n5. What are the exact court names you see? (e.g., 'Court #1, Court #2' or 'Court 1, Court 2'): ").strip()
            
            total_courts = input("\n6. How many courts total do you see?: ").strip()
            
            # SECTION 3: TIME SLOTS
            print("\n" + "="*60)
            print("SECTION 3: TIME SLOTS")
            print("="*60)
            
            time_layout = input("7. How are time slots displayed?\n   a) Horizontal timeline (times across the top)\n   b) Vertical timeline (times down the side)\n   c) In dropdown selectors\n   d) As clickable buttons\n   e) Other\n   Your answer: ").strip()
            
            time_format = input("\n8. What format are the times in?\n   a) 9:00 AM, 10:00 AM\n   b) 09:00, 10:00 (24-hour)\n   c) 9AM, 10AM\n   d) Other format\n   Your answer: ").strip()
            
            first_time = input("\n9. What is the FIRST time slot you see?: ").strip()
            last_time = input("\n10. What is the LAST time slot you see?: ").strip()
            
            # SECTION 4: AVAILABILITY INDICATORS
            print("\n" + "="*60)
            print("SECTION 4: AVAILABILITY INDICATORS")
            print("="*60)
            
            available_look = input("11. How do AVAILABLE slots look?\n   a) Green background\n   b) White/empty\n   c) Clickable button\n   d) Gray with text\n   e) Other\n   Your answer: ").strip()
            
            booked_look = input("\n12. How do BOOKED slots look?\n   a) Red background\n   b) Gray background\n   c) Text saying 'Booked'\n   d) Crossed out\n   e) Other\n   Your answer: ").strip()
            
            sample_available = input("\n13. Pick ONE specific available slot and tell me:\n   Court name: ").strip()
            sample_time = input("   Time: ").strip()
            sample_description = input("   What exactly does it say/look like?: ").strip()
            
            # SECTION 5: DATE NAVIGATION
            print("\n" + "="*60)
            print("SECTION 5: DATE NAVIGATION")
            print("="*60)
            
            date_nav_type = input("14. How can you change the date?\n   a) Dropdown next to current date\n   b) Calendar widget\n   c) Previous/Next arrows\n   d) Date input field\n   e) No date navigation visible\n   Your answer: ").strip()
            
            if date_nav_type.lower() != 'e':
                date_nav_location = input("\n15. Where exactly is the date navigation?\n   Describe the location: ").strip()
                
                # Test date navigation
                print(f"\n🔍 Let's test the date navigation...")
                print(f"Please try to change the date to tomorrow manually in the browser.")
                input(f"Press Enter when you've tried to change the date...")
                
                date_change_result = input(f"Did the date change work? (yes/no): ").strip().lower()
                
                if date_change_result == 'yes':
                    new_date_text = input(f"What does the date display show now?: ").strip()
                    new_url = page.url
                    print(f"New URL: {new_url}")
                else:
                    print(f"Date navigation didn't work - we'll need to investigate further")
            
            # SECTION 6: TECHNICAL DETAILS
            print("\n" + "="*60)
            print("SECTION 6: TECHNICAL DETAILS")
            print("="*60)
            
            current_url = page.url
            page_title = page.title()
            
            print(f"Current URL: {current_url}")
            print(f"Page title: {page_title}")
            
            # Try to find key elements
            print(f"\n🔍 Let me analyze the page structure...")
            
            # Count different types of elements
            buttons = page.locator("button").count()
            links = page.locator("a").count()
            inputs = page.locator("input").count()
            selects = page.locator("select").count()
            
            print(f"Technical analysis:")
            print(f"  - Buttons found: {buttons}")
            print(f"  - Links found: {links}")
            print(f"  - Input fields found: {inputs}")
            print(f"  - Select dropdowns found: {selects}")
            
            # Look for specific patterns
            time_elements = page.locator("*:has-text('AM'), *:has-text('PM')").count()
            court_elements = page.locator("*:has-text('Court')").count()
            booking_elements = page.locator("[class*='booking'], [class*='slot'], [class*='time']").count()
            
            print(f"  - Elements with AM/PM: {time_elements}")
            print(f"  - Elements with 'Court': {court_elements}")
            print(f"  - Booking-related elements: {booking_elements}")
            
            # SECTION 7: SUMMARY AND RECOMMENDATIONS
            print("\n" + "="*60)
            print("SECTION 7: SUMMARY")
            print("="*60)
            
            print(f"\n📊 Based on your answers:")
            print(f"  Layout: {layout_type}")
            print(f"  Current date: {current_date_text}")
            print(f"  Courts: {court_names} (total: {total_courts})")
            print(f"  Time range: {first_time} to {last_time}")
            print(f"  Available slots look: {available_look}")
            print(f"  Date navigation: {date_nav_type}")
            
            print(f"\n💡 Recommendations for fixing the agent:")
            
            # Generate specific recommendations
            if 'dropdown' in date_nav_type.lower():
                print(f"  ✅ Use dropdown-based date navigation")
            elif 'arrow' in date_nav_type.lower():
                print(f"  ✅ Use arrow-based date navigation")
            elif date_nav_type.lower() == 'e':
                print(f"  ⚠️  No date navigation visible - may be login-restricted")
            
            if 'calendar' in layout_type.lower():
                print(f"  ✅ Parse calendar grid structure")
            elif 'day' in layout_type.lower():
                print(f"  ✅ Parse day schedule structure")
            
            if 'horizontal' in court_layout.lower():
                print(f"  ✅ Look for courts in column headers")
            elif 'vertical' in court_layout.lower():
                print(f"  ✅ Look for courts in row headers")
            
            print(f"\n⏰ Browser will stay open for 30 seconds for final observation...")
            time.sleep(30)
            
        else:
            print(f"❌ Failed to load page: {nav_result}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
        
    print(f"\n📝 Next step: I'll use your answers to create custom selectors for your specific webpage structure.")

if __name__ == "__main__":
    inspect_webpage_structure()
