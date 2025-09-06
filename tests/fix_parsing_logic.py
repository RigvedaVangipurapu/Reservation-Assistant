#!/usr/bin/env python3
"""
Fix the parsing logic based on the debugging comparison
"""

from badminton_agent import BookingAgent
import time

def test_improved_parsing():
    """Test improved parsing logic"""
    
    print("🔧 FIXING PARSING LOGIC")
    print("=" * 40)
    print("Based on user feedback:")
    print("  • Should see 8 courts (not 1)")
    print("  • Should see ~25 slots (not 133)")
    print("  • Should detect the correct date")
    
    agent = BookingAgent(headless=False, slow_mo=1500)
    
    try:
        # Navigate to page
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("\n🔍 Testing improved element detection...")
            
            # Test different approaches to find actual booking slots
            page = agent.page
            
            # Method 1: Look for clickable time buttons
            print("\n📍 Method 1: Clickable elements with times")
            clickable_time_elements = page.locator("button:has-text('AM'), button:has-text('PM')")
            print(f"   Found {clickable_time_elements.count()} clickable time elements")
            
            # Method 2: Look for elements with specific time patterns and click handlers
            print("\n📍 Method 2: Elements with click handlers")
            interactive_elements = page.locator("[onclick], [role='button']:has-text('M')")
            print(f"   Found {interactive_elements.count()} interactive elements")
            
            # Method 3: Look for actual booking cells (grid structure)
            print("\n📍 Method 3: Grid/table structure")
            grid_cells = page.locator("td, .cell, [class*='grid-cell']")
            print(f"   Found {grid_cells.count()} grid cells")
            
            # Method 4: Look for elements that contain both court and time info
            print("\n📍 Method 4: Combined court + time elements")
            combined_elements = page.locator("*:has-text('Court'):has-text('M')")
            print(f"   Found {combined_elements.count()} combined elements")
            
            # Method 5: Look for available/bookable slots specifically
            print("\n📍 Method 5: Available/bookable indicators")
            available_elements = page.locator("[class*='available'], [class*='free'], .bookable")
            print(f"   Found {available_elements.count()} available elements")
            
            # Method 6: Look at the time column structure
            print("\n📍 Method 6: Time column analysis")
            time_elements = page.locator("[class*='time']")
            print(f"   Found {time_elements.count()} time elements")
            
            # Sample a few to see content
            if time_elements.count() > 0:
                print("   Sample time elements:")
                for i in range(min(3, time_elements.count())):
                    element = time_elements.nth(i)
                    text = element.text_content() or ""
                    classes = element.get_attribute("class") or ""
                    print(f"     {i+1}. Text: {repr(text[:50])}")
                    print(f"        Classes: {classes}")
            
            # Method 7: Look for the actual schedule grid
            print("\n📍 Method 7: Schedule grid detection")
            schedule_containers = page.locator("[class*='schedule'], [class*='calendar'], [class*='timetable']")
            print(f"   Found {schedule_containers.count()} schedule containers")
            
            # Method 8: Check for the specific Skedda structure
            print("\n📍 Method 8: Skedda-specific structure")
            
            # Look for day view vs grid view
            day_view = page.locator("[class*='day-view'], [class*='day-mode']")
            grid_view = page.locator("[class*='grid-view'], [class*='grid-mode']")
            print(f"   Day view elements: {day_view.count()}")
            print(f"   Grid view elements: {grid_view.count()}")
            
            # Check what view mode we're in
            page_text = page.inner_text("body")
            if "Day" in page_text and "Grid" in page_text:
                print("   📋 Both Day and Grid view options available")
                
                # Try switching to Grid view for better parsing
                grid_button = page.locator("button:has-text('Grid'), [role='button']:has-text('Grid')")
                if grid_button.count() > 0:
                    print("   🔄 Switching to Grid view...")
                    grid_button.first.click()
                    time.sleep(3)
                    
                    # Re-analyze after switching
                    booking_elements_after = page.locator("[class*='booking']")
                    print(f"   After Grid switch: {booking_elements_after.count()} booking elements")
            
            # Method 9: Look for the actual time slots in the current view
            print("\n📍 Method 9: Current view slot analysis")
            
            # Find elements that look like actual bookable slots
            slot_candidates = page.locator("button[class*='slot'], [class*='time-slot'], [data-time], button:has-text(':')").filter(visible=True)
            print(f"   Visible slot candidates: {slot_candidates.count()}")
            
            if slot_candidates.count() > 0:
                print("   📋 Sample slot candidates:")
                for i in range(min(5, slot_candidates.count())):
                    element = slot_candidates.nth(i)
                    text = element.text_content() or ""
                    classes = element.get_attribute("class") or ""
                    print(f"     {i+1}. Text: {repr(text[:30])}")
                    print(f"        Classes: {classes}")
                    print(f"        Clickable: {element.is_enabled()}")
            
            print("\n📊 ANALYSIS COMPLETE")
            print("Based on this analysis, I can create improved parsing logic")
            print("that focuses on the actual bookable elements you see.")
            
            time.sleep(10)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    test_improved_parsing()
