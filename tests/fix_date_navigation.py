#!/usr/bin/env python3
"""
Fix the date navigation by finding the correct Skedda date controls
"""

from badminton_agent import BookingAgent
import time

def fix_date_navigation():
    """Find and test different date navigation methods"""
    
    print("🔧 FIXING DATE NAVIGATION")
    print("=" * 40)
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            page = agent.page
            
            print("🔍 Searching for date navigation controls...")
            
            # Method 1: Look for date picker input fields
            print("\n📅 Method 1: Date picker inputs")
            date_inputs = page.locator("input[type='date'], input[placeholder*='date'], input[name*='date']")
            print(f"   Found {date_inputs.count()} date input fields")
            
            # Method 2: Look for calendar navigation arrows
            print("\n📅 Method 2: Calendar navigation arrows")
            nav_arrows = page.locator("button:has-text('>'), button:has-text('<'), button:has-text('›'), button:has-text('‹'), [class*='next'], [class*='prev'], [class*='forward'], [class*='back']")
            print(f"   Found {nav_arrows.count()} navigation arrows")
            
            if nav_arrows.count() > 0:
                print("   Sample navigation elements:")
                for i in range(min(3, nav_arrows.count())):
                    element = nav_arrows.nth(i)
                    text = element.text_content() or ""
                    classes = element.get_attribute("class") or ""
                    print(f"     {i+1}. Text: {repr(text)}, Classes: {classes}")
            
            # Method 3: Look for clickable date elements
            print("\n📅 Method 3: Clickable date elements")
            date_elements = page.locator("*:has-text('September'), *:has-text('2025'), [class*='date'], [class*='calendar']")
            clickable_dates = date_elements.filter(visible=True)
            print(f"   Found {clickable_dates.count()} visible date-related elements")
            
            # Method 4: Look for day/week navigation
            print("\n📅 Method 4: Day/week navigation")
            day_nav = page.locator("button:has-text('Next'), button:has-text('Previous'), button:has-text('Tomorrow'), button:has-text('Today')")
            print(f"   Found {day_nav.count()} day navigation buttons")
            
            # Method 5: URL manipulation
            print("\n📅 Method 5: URL manipulation")
            current_url = page.url
            print(f"   Current URL: {current_url}")
            
            # Try URL with date parameter
            test_url = "https://ocbadminton.skedda.com/booking?date=2025-09-06"
            print(f"   Trying direct URL navigation to: {test_url}")
            
            page.goto(test_url)
            time.sleep(3)
            
            new_url = page.url
            print(f"   New URL: {new_url}")
            
            # Check if this worked
            page_text = page.inner_text("body")
            if "6" in page_text and "September" in page_text:
                print("   ✅ URL navigation might have worked!")
            else:
                print("   ❌ URL navigation didn't work")
            
            # Method 6: Try different URL formats
            print("\n📅 Method 6: Different URL formats")
            
            url_formats = [
                "https://ocbadminton.skedda.com/booking?nbstart=2025-09-06T09:00:00",
                "https://ocbadminton.skedda.com/booking?nbend=2025-09-06T21:00:00&nbstart=2025-09-06T09:00:00",
                "https://ocbadminton.skedda.com/booking#2025-09-06"
            ]
            
            for url_format in url_formats:
                print(f"   Trying: {url_format}")
                page.goto(url_format)
                time.sleep(2)
                
                current_text = page.inner_text("body")
                if "6" in current_text and ("September" in current_text or "Sep" in current_text):
                    print(f"   ✅ This format worked!")
                    break
                else:
                    print(f"   ❌ This format didn't work")
            
            # Method 7: JavaScript date manipulation
            print("\n📅 Method 7: JavaScript manipulation")
            
            try:
                # Try to find and manipulate date-related JavaScript
                result = page.evaluate("""
                () => {
                    // Look for date-related global variables
                    const dateVars = [];
                    for (let prop in window) {
                        if (prop.toLowerCase().includes('date') || prop.toLowerCase().includes('calendar')) {
                            dateVars.push(prop);
                        }
                    }
                    return dateVars;
                }
                """)
                print(f"   Found JS date variables: {result}")
            except:
                print("   ❌ JS date variable search failed")
            
            # Method 8: Look for actual working date controls
            print("\n📅 Method 8: Interactive date control search")
            
            # Look for elements that might change dates when clicked
            potential_controls = page.locator("button, a, [onclick], [role='button']").filter(visible=True)
            
            print(f"   Found {potential_controls.count()} interactive elements")
            
            # Test a few by examining their text/attributes
            if potential_controls.count() > 0:
                print("   Examining first 10 interactive elements for date controls:")
                for i in range(min(10, potential_controls.count())):
                    element = potential_controls.nth(i)
                    text = (element.text_content() or "").strip()
                    onclick = element.get_attribute("onclick") or ""
                    
                    if any(keyword in text.lower() for keyword in ['next', 'prev', 'forward', 'back', 'day', 'date']) or \
                       any(keyword in onclick.lower() for keyword in ['date', 'day', 'calendar']):
                        print(f"     {i+1}. Text: {repr(text[:30])}, OnClick: {repr(onclick[:50])}")
                        
                        # Try clicking this element
                        try:
                            print(f"        🖱️  Trying to click this element...")
                            element.click()
                            time.sleep(2)
                            
                            # Check if anything changed
                            new_text = page.inner_text("body")
                            if new_text != page_text:
                                print(f"        ✅ Page changed after clicking!")
                                break
                            else:
                                print(f"        ❌ No change after clicking")
                        except:
                            print(f"        ❌ Could not click element")
            
            print("\n👀 FINAL CHECK:")
            print("Look at the browser now. What date is displayed?")
            print("Did any of the navigation attempts work?")
            
            time.sleep(15)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    fix_date_navigation()
