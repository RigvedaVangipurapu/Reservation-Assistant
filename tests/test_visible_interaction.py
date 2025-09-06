#!/usr/bin/env python3
"""
Test visible browser interactions - you should see everything happening
"""

from badminton_agent import BookingAgent
import time

def test_visible_interactions():
    """Test with visible browser interactions"""
    
    print("🎬 VISIBLE BROWSER INTERACTION TEST")
    print("=" * 50)
    print("You should see a Chromium browser window open and watch the agent interact with it")
    
    # Create agent with visible browser and slow actions
    agent = BookingAgent(
        headless=False,        # Browser will be visible
        slow_mo=2000          # 2 second delay between actions
    )
    
    try:
        print("\n🌐 Step 1: Opening booking page (you should see browser open)...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("   ✅ Page loaded - you should see the Skedda booking page")
            
            print("\n⏰ Step 2: Waiting 5 seconds for you to observe the page...")
            time.sleep(5)
            
            print("\n🔍 Step 3: Let's try to click on different elements...")
            
            page = agent.page
            
            # Test 1: Try to click on a time slot
            print("   🎯 Trying to click on time elements...")
            time_elements = page.locator("button:has-text('AM'), button:has-text('PM')")
            
            if time_elements.count() > 0:
                print(f"   Found {time_elements.count()} time elements")
                print("   Clicking on the first one...")
                
                # Highlight the element first
                first_time_element = time_elements.first
                
                # Add visual highlight
                page.evaluate("""
                (element) => {
                    element.style.border = '3px solid red';
                    element.style.backgroundColor = 'yellow';
                }
                """, first_time_element)
                
                print("   🔴 Element highlighted in red/yellow - can you see it?")
                time.sleep(3)
                
                # Click it
                print("   👆 Clicking now...")
                first_time_element.click()
                time.sleep(3)
                
                print("   ✅ Click completed - did you see any changes?")
                
            else:
                print("   ❌ No time elements found to click")
            
            # Test 2: Try clicking on booking elements
            print("\n   🎯 Trying to click on booking elements...")
            booking_elements = page.locator("[class*='booking']").filter(visible=True)
            
            if booking_elements.count() > 0:
                print(f"   Found {booking_elements.count()} visible booking elements")
                
                # Try clicking on a few
                for i in range(min(3, booking_elements.count())):
                    print(f"   Highlighting and clicking element {i+1}...")
                    
                    element = booking_elements.nth(i)
                    
                    # Highlight
                    page.evaluate("""
                    (element) => {
                        element.style.border = '3px solid blue';
                        element.style.backgroundColor = 'lightblue';
                    }
                    """, element)
                    
                    time.sleep(2)
                    
                    try:
                        element.click()
                        print(f"   ✅ Clicked element {i+1}")
                    except:
                        print(f"   ❌ Could not click element {i+1}")
                    
                    time.sleep(2)
            
            # Test 3: Try switching view modes
            print("\n   🎯 Trying to switch view modes...")
            
            # Look for Grid/Day buttons
            grid_button = page.locator("button:has-text('Grid')")
            day_button = page.locator("button:has-text('Day')")
            
            if grid_button.count() > 0:
                print("   Found Grid button - highlighting and clicking...")
                
                page.evaluate("""
                (element) => {
                    element.style.border = '5px solid green';
                    element.style.backgroundColor = 'lightgreen';
                }
                """, grid_button.first)
                
                time.sleep(3)
                grid_button.first.click()
                print("   ✅ Clicked Grid button")
                time.sleep(3)
            
            if day_button.count() > 0:
                print("   Found Day button - highlighting and clicking...")
                
                page.evaluate("""
                (element) => {
                    element.style.border = '5px solid orange';
                    element.style.backgroundColor = 'lightyellow';
                }
                """, day_button.first)
                
                time.sleep(3)
                day_button.first.click()
                print("   ✅ Clicked Day button")
                time.sleep(3)
            
            # Test 4: Try date navigation
            print("\n   🎯 Trying date navigation...")
            
            date_nav_buttons = page.locator("button:has-text('>'), button:has-text('<'), button:has-text('›'), button:has-text('‹')")
            
            if date_nav_buttons.count() > 0:
                print(f"   Found {date_nav_buttons.count()} date navigation buttons")
                
                for i in range(min(2, date_nav_buttons.count())):
                    button = date_nav_buttons.nth(i)
                    
                    # Highlight
                    page.evaluate("""
                    (element) => {
                        element.style.border = '3px solid purple';
                        element.style.backgroundColor = 'lavender';
                    }
                    """, button)
                    
                    time.sleep(2)
                    
                    try:
                        button.click()
                        print(f"   ✅ Clicked date navigation button {i+1}")
                        time.sleep(3)
                    except:
                        print(f"   ❌ Could not click date navigation button {i+1}")
            
            print("\n👀 OBSERVATION TIME")
            print("The browser will stay open for 30 seconds.")
            print("Please tell me:")
            print("  • Did you see the browser window open?")
            print("  • Did you see elements being highlighted in colors?")
            print("  • Did you see any clicks happening?")
            print("  • Did the page change when buttons were clicked?")
            print("  • What view mode is currently active (Day/Grid)?")
            
            time.sleep(30)
            
        else:
            print(f"   ❌ Failed to load page: {nav_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        
    finally:
        print("\n🔴 Closing browser...")
        agent.stop_browser()
    
    print("\n📝 What did you observe?")
    print("If you couldn't see the interactions, there might be an issue with:")
    print("  • Browser visibility settings")
    print("  • Window focus/positioning")
    print("  • Display/monitor configuration")

if __name__ == "__main__":
    test_visible_interactions()
