#!/usr/bin/env python3
"""
Improve availability detection to distinguish between available and booked slots
"""

from badminton_agent import BookingAgent
import time

def analyze_booking_elements():
    """Analyze the actual booking elements to understand available vs booked"""
    
    print("🔬 ANALYZING BOOKING ELEMENTS")
    print("=" * 50)
    print("Let's understand how to distinguish available from booked slots")
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("\n🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            page = agent.page
            
            print("✅ Page loaded")
            print("\n🔍 DEEP ANALYSIS OF BOOKING ELEMENTS...")
            
            # Let's examine booking elements more carefully
            booking_elements = page.locator("[class*='booking']").filter(visible=True)
            print(f"Found {booking_elements.count()} visible booking elements")
            
            # Look at each element in detail
            for i in range(min(10, booking_elements.count())):
                element = booking_elements.nth(i)
                
                print(f"\n📋 Element {i+1}:")
                try:
                    # Get all attributes
                    classes = element.get_attribute("class") or ""
                    text = element.text_content() or ""
                    style = element.get_attribute("style") or ""
                    title = element.get_attribute("title") or ""
                    
                    print(f"   Classes: {classes}")
                    print(f"   Text: {repr(text[:100])}")
                    print(f"   Style: {style}")
                    print(f"   Title: {title}")
                    
                    # Check if element is clickable
                    is_enabled = element.is_enabled()
                    is_visible = element.is_visible()
                    
                    print(f"   Enabled: {is_enabled}")
                    print(f"   Visible: {is_visible}")
                    
                    # Look for availability indicators in classes
                    availability_indicators = []
                    if "available" in classes.lower():
                        availability_indicators.append("available-class")
                    if "booked" in classes.lower():
                        availability_indicators.append("booked-class")
                    if "occupied" in classes.lower():
                        availability_indicators.append("occupied-class")
                    if "free" in classes.lower():
                        availability_indicators.append("free-class")
                    if "disabled" in classes.lower():
                        availability_indicators.append("disabled-class")
                    
                    print(f"   Availability indicators: {availability_indicators}")
                    
                    # Check background color
                    try:
                        bg_color = page.evaluate("element => window.getComputedStyle(element).backgroundColor", element)
                        color = page.evaluate("element => window.getComputedStyle(element).color", element)
                        print(f"   Background color: {bg_color}")
                        print(f"   Text color: {color}")
                    except:
                        print(f"   Could not get computed styles")
                    
                except Exception as e:
                    print(f"   Error analyzing element: {e}")
            
            print(f"\n🎯 SPECIFIC SLOT ANALYSIS:")
            print(f"Now let's examine specific slots you identified in the comparison...")
            
            # Test specific slots from the comparison
            test_slots = [
                ("Court #1", "10:00 AM", "booked"),
                ("Court #2", "9:00 AM", "available"), 
                ("Court #3", "9:00 AM", "booked"),
                ("Court #8", "9:00 AM", "available")
            ]
            
            for court, time_slot, expected_status in test_slots:
                print(f"\n🔍 Analyzing {court} at {time_slot} (expected: {expected_status}):")
                
                # Try to find elements that might represent this slot
                selectors_to_try = [
                    f"*:has-text('{court}'):has-text('{time_slot}')",
                    f"*:has-text('{time_slot}'):near(*:has-text('{court}'))",
                    f"*:has-text('{time_slot.split()[0]}')",  # Just the time part
                    f"[title*='{time_slot}']",
                    f"[aria-label*='{time_slot}']"
                ]
                
                found_elements = []
                for selector in selectors_to_try:
                    try:
                        elements = page.locator(selector).filter(visible=True)
                        if elements.count() > 0:
                            found_elements.append((selector, elements))
                            print(f"   Found with selector: {selector} ({elements.count()} elements)")
                    except:
                        continue
                
                if found_elements:
                    # Examine the first match
                    selector, elements = found_elements[0]
                    element = elements.first
                    
                    try:
                        classes = element.get_attribute("class") or ""
                        text = element.text_content() or ""
                        style = element.get_attribute("style") or ""
                        
                        print(f"   Element details:")
                        print(f"     Classes: {classes}")
                        print(f"     Text: {repr(text[:50])}")
                        print(f"     Style: {style}")
                        
                        # Check if it looks available or booked
                        likely_status = "unknown"
                        
                        # Check for availability indicators
                        if any(word in classes.lower() for word in ["available", "free", "open"]):
                            likely_status = "available"
                        elif any(word in classes.lower() for word in ["booked", "occupied", "taken", "disabled"]):
                            likely_status = "booked"
                        elif "white" in style.lower() or "transparent" in style.lower():
                            likely_status = "available"
                        elif "gray" in style.lower() or "grey" in style.lower():
                            likely_status = "booked"
                        
                        print(f"     Likely status: {likely_status}")
                        print(f"     Expected: {expected_status}")
                        
                        if likely_status == expected_status:
                            print(f"     ✅ Match!")
                        else:
                            print(f"     ❌ Mismatch")
                        
                    except Exception as e:
                        print(f"   Error examining element: {e}")
                else:
                    print(f"   ❌ No elements found for this slot")
            
            print(f"\n💡 RECOMMENDATIONS:")
            print(f"Based on this analysis, I can improve the availability detection by:")
            print(f"   • Looking for specific CSS classes that indicate booking status")
            print(f"   • Checking background colors (white=available, gray=booked)")
            print(f"   • Using computed styles to determine availability")
            print(f"   • Better element selection logic")
            
            print(f"\n⏰ Browser staying open for 30 seconds for observation...")
            time.sleep(30)
            
        else:
            print(f"❌ Failed to load page")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    analyze_booking_elements()
