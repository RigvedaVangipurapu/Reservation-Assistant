#!/usr/bin/env python3
"""
Simple visual test - just basic clicking without highlighting
"""

from badminton_agent import BookingAgent
import time

def simple_visual_test():
    """Simple test with basic clicking"""
    
    print("👁️  SIMPLE VISUAL TEST")
    print("=" * 30)
    print("Browser should open and you should see basic interactions")
    
    # Create agent with very visible settings
    agent = BookingAgent(
        headless=False,        # Visible browser
        slow_mo=3000          # 3 second delay between actions
    )
    
    try:
        print("\n🌐 Opening page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded")
            print("\n👀 LOOK AT THE BROWSER WINDOW NOW")
            print("You should see the Skedda booking page")
            
            # Give time to observe
            time.sleep(5)
            
            page = agent.page
            
            print("\n🔍 Looking for clickable elements...")
            
            # Try simple clicks on different types of elements
            
            # 1. Try clicking any button
            buttons = page.locator("button").filter(visible=True)
            print(f"Found {buttons.count()} visible buttons")
            
            if buttons.count() > 0:
                print("Clicking first button...")
                try:
                    buttons.first.click()
                    print("✅ Button clicked")
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ Button click failed: {e}")
            
            # 2. Try clicking elements with text containing time
            time_text_elements = page.locator("*:has-text('AM'), *:has-text('PM')").filter(visible=True)
            print(f"Found {time_text_elements.count()} elements with AM/PM")
            
            if time_text_elements.count() > 0:
                print("Clicking first time element...")
                try:
                    time_text_elements.first.click()
                    print("✅ Time element clicked")
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ Time element click failed: {e}")
            
            # 3. Try scrolling to see more content
            print("Scrolling down...")
            try:
                page.evaluate("window.scrollBy(0, 300)")
                time.sleep(2)
                print("✅ Scrolled down")
            except Exception as e:
                print(f"❌ Scroll failed: {e}")
            
            # 4. Try clicking on specific view buttons
            print("Looking for Grid/Day buttons...")
            
            # Check current page state
            current_url = page.url
            page_title = page.title()
            print(f"Current URL: {current_url}")
            print(f"Page title: {page_title}")
            
            # Look for navigation elements
            nav_elements = page.locator("nav, .nav, [role='navigation']").filter(visible=True)
            print(f"Found {nav_elements.count()} navigation elements")
            
            # Try to find and click view mode buttons
            possible_view_buttons = page.locator("button:has-text('Grid'), button:has-text('Day')").filter(visible=True)
            print(f"Found {possible_view_buttons.count()} view mode buttons")
            
            if possible_view_buttons.count() > 0:
                print("Trying to click view mode button...")
                try:
                    possible_view_buttons.first.click()
                    print("✅ View mode button clicked")
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ View mode button click failed: {e}")
            
            print("\n📊 Current page analysis:")
            
            # Get current state
            state_result = agent.get_current_page_state()
            print(f"Courts detected: {state_result.get('courts_found', 0)}")
            print(f"Booking elements: {state_result.get('booking_elements', 0)}")
            
            # Check what's actually visible
            all_visible_elements = page.locator("*").filter(visible=True)
            print(f"Total visible elements: {all_visible_elements.count()}")
            
            print("\n🔍 Let me try our booking slot detection...")
            slots_result = agent.get_available_slots()
            print(f"Slots found: {slots_result.get('total_slots', 0)}")
            print(f"Available: {slots_result.get('available_slots', 0)}")
            
            if slots_result.get("slots"):
                print("\nFirst 3 detected slots:")
                for i, slot in enumerate(slots_result["slots"][:3], 1):
                    print(f"  {i}. {slot.get('court', 'Unknown')} - {slot.get('time', 'Unknown')}")
            
            print(f"\n⏰ Browser will stay open for 20 more seconds...")
            print("Please observe:")
            print("  • Can you see the browser window?")
            print("  • What view mode is currently active?")
            print("  • How many courts do you actually see?")
            print("  • How many time slots look clickable/available?")
            
            time.sleep(20)
            
        else:
            print(f"❌ Navigation failed: {nav_result}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🔴 Closing browser...")
        agent.stop_browser()

if __name__ == "__main__":
    simple_visual_test()
