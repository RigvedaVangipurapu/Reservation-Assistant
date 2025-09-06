#!/usr/bin/env python3
"""
Improve the booking agent for visitor mode operation
"""

from badminton_agent import BookingAgent
from datetime import datetime, timedelta

def test_visitor_mode_improvements():
    """Test improved visitor mode handling"""
    
    print("🔍 Improving Visitor Mode Operation")
    print("=" * 50)
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("🌐 1. Navigating to booking page...")
        nav_result = agent.navigate_to_booking()
        
        print("\n📊 2. Analyzing visitor mode limitations...")
        state_result = agent.get_current_page_state()
        
        print("\n📅 3. Testing date functionality in visitor mode...")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"   Trying to change to: {tomorrow}")
        
        # Try different date change approaches
        date_result = agent.change_date(target_date=tomorrow)
        print(f"   Standard date change: {date_result['success']}")
        
        if not date_result["success"]:
            print("   Trying alternative date change methods...")
            
            # Method 1: Try clicking date navigation arrows
            try:
                next_day_buttons = agent.page.locator("button:has-text('›'), button:has-text('>'), [class*='next'], [class*='forward']")
                if next_day_buttons.count() > 0:
                    print("   Found next day button, clicking...")
                    next_day_buttons.first.click()
                    import time
                    time.sleep(3)
                    print("   ✅ Clicked next day button")
                else:
                    print("   ❌ No next day button found")
            except Exception as e:
                print(f"   ❌ Next day button error: {e}")
            
            # Method 2: Try URL manipulation
            try:
                current_url = agent.page.url
                if "date=" in current_url:
                    new_url = current_url.replace(current_url.split("date=")[1].split("&")[0], tomorrow)
                    print(f"   Trying URL manipulation: {new_url}")
                    agent.page.goto(new_url)
                    time.sleep(3)
                    print("   ✅ URL manipulation attempted")
            except Exception as e:
                print(f"   ❌ URL manipulation error: {e}")
        
        print("\n🔍 4. Analyzing what data is actually available...")
        
        # Get more detailed information about what we can see
        page_text_result = agent.get_page_text(max_length=3000)
        if page_text_result["success"]:
            page_text = page_text_result["text"]
            
            # Extract useful information from visitor mode
            print("   📄 Extracting available information:")
            
            # Look for time slots
            import re
            time_matches = re.findall(r'\d{1,2}:\d{2}\s*[AP]M', page_text)
            if time_matches:
                unique_times = list(set(time_matches))
                print(f"   ⏰ Times found: {unique_times[:10]}")  # Show first 10
            
            # Look for court information
            court_matches = re.findall(r'Court\s*#?\d+', page_text)
            if court_matches:
                unique_courts = list(set(court_matches))
                print(f"   🏸 Courts found: {unique_courts}")
            
            # Look for date information
            date_matches = re.findall(r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)[^,]*\d{4}', page_text)
            if date_matches:
                print(f"   📅 Date info: {date_matches}")
            
            # Check for any availability indicators
            availability_keywords = ['available', 'booked', 'reserved', 'free']
            found_keywords = [kw for kw in availability_keywords if kw.lower() in page_text.lower()]
            if found_keywords:
                print(f"   🎯 Availability keywords: {found_keywords}")
            
            # Look for visitor mode warnings
            if "VISITOR MODE" in page_text:
                print("   ⚠️  Confirmed: Running in VISITOR MODE")
                print("   💡 This means limited data visibility")
            
            if "LIMITED VISIBILITY" in page_text:
                print("   ⚠️  Confirmed: LIMITED VISIBILITY mode")
        
        print("\n🔧 5. Testing improved slot detection...")
        slots_result = agent.get_available_slots()
        
        if slots_result["success"]:
            total_slots = slots_result.get("total_slots", 0)
            available_slots = slots_result.get("available_slots", 0)
            
            print(f"   📊 Raw data: {total_slots} total, {available_slots} available")
            
            # Analyze if this looks realistic
            if available_slots == total_slots and total_slots > 50:
                print("   ⚠️  Warning: All slots appear available (likely visitor mode placeholder data)")
            elif available_slots == 0:
                print("   ⚠️  Warning: No slots available (possible parsing issue)")
            else:
                print("   ✅ Data looks realistic")
            
            # Show sample data
            if slots_result.get("slots"):
                print("   📋 Sample slots:")
                for i, slot in enumerate(slots_result["slots"][:3]):
                    print(f"      {i+1}. {slot}")
        
        print("\n💡 6. Recommendations for visitor mode:")
        print("   • Add disclaimer about limited data accuracy")
        print("   • Focus on showing general availability patterns")
        print("   • Warn users that actual availability may differ")
        print("   • Provide link to check website directly")
        print("   • Use data for general planning, not exact booking")
        
        print("\n⏰ Browser staying open for 20 seconds for manual inspection...")
        import time
        time.sleep(20)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    test_visitor_mode_improvements()
