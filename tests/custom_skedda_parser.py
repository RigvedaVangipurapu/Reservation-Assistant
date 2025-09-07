#!/usr/bin/env python3
"""
Custom Skedda parser based on your specific webpage structure
"""

from badminton_agent import BookingAgent
import time
import re
from datetime import datetime

def create_custom_parser(agent):
    """Create custom parsing logic for your specific Skedda layout"""
    
    class CustomSkeddaParser:
        def __init__(self, page):
            self.page = page
            
        def get_current_date(self):
            """Extract current date from the top center display"""
            try:
                # Look for the exact date format you see
                page_text = self.page.inner_text("body")
                
                # Pattern for "FRIDAY, SEPTEMBER 5, 2025"
                date_pattern = r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),\s+([A-Z]+)\s+(\d+),\s+(\d{4})'
                match = re.search(date_pattern, page_text)
                
                if match:
                    weekday, month, day, year = match.groups()
                    
                    # Convert month name to number
                    months = {
                        'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4,
                        'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8,
                        'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
                    }
                    
                    month_num = months.get(month, 1)
                    return f"{year}-{month_num:02d}-{int(day):02d}"
                
                return None
            except:
                return None
        
        def change_date_via_dropdown(self, target_date):
            """Change date using the dropdown arrow next to the date"""
            try:
                print(f"🔽 Looking for date dropdown...")
                
                # Look for clickable date elements or arrows near the date
                date_selectors = [
                    # Look for elements containing the current date
                    "*:has-text('SEPTEMBER'):has-text('2025')",
                    # Look for dropdown arrows or buttons
                    "button[class*='date']",
                    "[class*='dropdown']:has-text('SEPTEMBER')",
                    # Look for clickable elements near date text
                    "*:has-text('FRIDAY') button",
                    "*:has-text('SATURDAY') button",
                    # Generic dropdown indicators
                    "[class*='arrow'], [class*='chevron'], [class*='expand']"
                ]
                
                for selector in date_selectors:
                    elements = self.page.locator(selector)
                    if elements.count() > 0:
                        print(f"🎯 Found potential date control: {selector}")
                        
                        # Try clicking the first match
                        elements.first.click()
                        time.sleep(2)
                        
                        # Look for date options that appeared
                        target_dt = datetime.strptime(target_date, "%Y-%m-%d")
                        
                        # Try different ways to find the target date
                        date_options = [
                            f"*:has-text('{target_dt.day}')",
                            f"*:has-text('{target_dt.strftime('%B')}')",
                            f"*:has-text('{target_dt.strftime('%A')}')",
                            f"option:has-text('{target_dt.day}')"
                        ]
                        
                        for option_selector in date_options:
                            options = self.page.locator(option_selector)
                            if options.count() > 0:
                                print(f"📅 Clicking date option: {option_selector}")
                                options.first.click()
                                time.sleep(2)
                                return True
                        
                        # If no specific date found, try just clicking next day
                        next_buttons = self.page.locator("button:has-text('>'), *:has-text('Next'), *:has-text('Forward')")
                        if next_buttons.count() > 0:
                            print(f"⏭️ Clicking next button")
                            next_buttons.first.click()
                            time.sleep(2)
                            return True
                
                return False
                
            except Exception as e:
                print(f"❌ Date change error: {e}")
                return False
        
        def get_all_courts(self):
            """Get list of all courts (horizontal layout)"""
            try:
                courts = []
                
                # Based on your input: Court #1 through Court #8
                for i in range(1, 9):
                    courts.append(f"Court #{i}")
                
                # Verify courts exist on page
                page_text = self.page.inner_text("body")
                verified_courts = []
                for court in courts:
                    if court in page_text:
                        verified_courts.append(court)
                
                print(f"🏸 Found courts: {verified_courts}")
                return verified_courts
                
            except Exception as e:
                print(f"❌ Court detection error: {e}")
                return []
        
        def get_available_time_slots(self, court_name):
            """Get available time slots for a specific court"""
            try:
                slots = []
                
                # Look for time elements in the vertical timeline
                # Based on your input: times are in format "11:00 AM - 12:00 PM"
                
                # Find all time range elements
                time_pattern = r'(\d{1,2}:\d{2}\s+[AP]M)\s*[-–]\s*(\d{1,2}:\d{2}\s+[AP]M)'
                page_text = self.page.inner_text("body")
                
                time_matches = re.findall(time_pattern, page_text)
                
                # For each time range, check if it's available for this court
                for start_time, end_time in time_matches:
                    # Look for elements that contain both the court name and this time
                    time_range = f"{start_time} - {end_time}"
                    
                    # Try to find clickable elements for this time slot
                    time_selectors = [
                        f"*:has-text('{start_time}'):has-text('{court_name}')",
                        f"*:has-text('{time_range}'):has-text('{court_name}')",
                        f"*:has-text('{start_time}')",  # Fallback to just time
                    ]
                    
                    for selector in time_selectors:
                        elements = self.page.locator(selector).filter(visible=True)
                        if elements.count() > 0:
                            # Check if this appears to be an available slot (white/empty background)
                            element = elements.first
                            
                            # Check if it's clickable/available
                            is_clickable = element.is_enabled() if hasattr(element, 'is_enabled') else True
                            
                            if is_clickable:
                                slots.append({
                                    'court': court_name,
                                    'start_time': start_time,
                                    'end_time': end_time,
                                    'time_range': time_range,
                                    'available': True
                                })
                                break
                
                return slots
                
            except Exception as e:
                print(f"❌ Time slot detection error: {e}")
                return []
        
        def get_all_available_slots(self):
            """Get all available slots for all courts"""
            try:
                all_slots = []
                courts = self.get_all_courts()
                
                for court in courts:
                    court_slots = self.get_available_time_slots(court)
                    all_slots.extend(court_slots)
                
                return all_slots
                
            except Exception as e:
                print(f"❌ Slot detection error: {e}")
                return []
    
    return CustomSkeddaParser(agent.page)

def test_custom_parser():
    """Test the custom parser with your specific webpage"""
    
    print("🧪 TESTING CUSTOM SKEDDA PARSER")
    print("=" * 50)
    
    agent = BookingAgent(headless=False, slow_mo=1500)
    
    try:
        print("🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            parser = create_custom_parser(agent)
            
            print("\n📅 Testing date detection...")
            current_date = parser.get_current_date()
            print(f"Current date: {current_date}")
            
            print("\n🏸 Testing court detection...")
            courts = parser.get_all_courts()
            print(f"Courts found: {courts}")
            
            print("\n⏰ Testing time slot detection...")
            if courts:
                # Test with first court
                test_court = courts[0]
                slots = parser.get_available_time_slots(test_court)
                print(f"Slots for {test_court}: {len(slots)} found")
                
                if slots:
                    print("Sample slots:")
                    for i, slot in enumerate(slots[:3], 1):
                        print(f"  {i}. {slot['time_range']} - Available: {slot['available']}")
            
            print("\n📊 Testing full availability scan...")
            all_slots = parser.get_all_available_slots()
            print(f"Total available slots found: {len(all_slots)}")
            
            # Group by court for summary
            court_summary = {}
            for slot in all_slots:
                court = slot['court']
                if court not in court_summary:
                    court_summary[court] = 0
                court_summary[court] += 1
            
            print("Slots per court:")
            for court, count in court_summary.items():
                print(f"  {court}: {count} slots")
            
            print("\n🔄 Testing date navigation...")
            print("I'll try to change to tomorrow using the dropdown...")
            
            tomorrow = datetime.now().strftime("%Y-%m-%d")
            if current_date:
                # Calculate tomorrow from current date
                current_dt = datetime.strptime(current_date, "%Y-%m-%d")
                tomorrow_dt = datetime.fromordinal(current_dt.toordinal() + 1)
                tomorrow = tomorrow_dt.strftime("%Y-%m-%d")
            
            success = parser.change_date_via_dropdown(tomorrow)
            print(f"Date change success: {success}")
            
            if success:
                time.sleep(3)
                new_date = parser.get_current_date()
                print(f"New date: {new_date}")
            
            print("\n⏰ Browser staying open for 20 seconds for observation...")
            time.sleep(20)
            
        else:
            print(f"❌ Failed to load page: {nav_result}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Custom parser testing complete!")
    print("Based on the results, I can now update the main agent with the correct selectors.")

if __name__ == "__main__":
    test_custom_parser()
