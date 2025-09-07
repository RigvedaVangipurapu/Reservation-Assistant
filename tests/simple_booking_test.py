#!/usr/bin/env python3
"""
Simple test to gather essential booking interface information
"""

from playwright.sync_api import sync_playwright
import time

def simple_booking_test():
    """Gather essential information about the Skedda booking interface"""
    
    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(30000)
        
        try:
            print("🌐 Loading booking page...")
            page.goto("https://ocbadminton.skedda.com/booking")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)
            
            print("✅ Page loaded")
            
            # Get current page structure
            print("\n🔍 Analyzing page structure...")
            
            # Check what courts are visible
            print("🏸 Looking for courts...")
            court_headers = page.locator("[class*='header'], [class*='label']:has-text('Court')")
            print(f"   Found {court_headers.count()} court headers")
            
            # Look for any clickable time slots or booking elements
            print("🕐 Looking for time slots...")
            
            # Different possible selectors for booking slots
            slot_selectors = [
                "[class*='booking']",
                "[class*='slot']", 
                "[class*='time']",
                "[data-bs-toggle]",
                "[onclick]",
                "button:not([class*='dropdown'])"
            ]
            
            for selector in slot_selectors:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    print(f"   📍 Selector '{selector}': {count} elements")
                    
                    # Get sample text from first few elements
                    for i in range(min(3, count)):
                        try:
                            text = elements.nth(i).text_content()
                            if text and len(text.strip()) > 0 and len(text.strip()) < 100:
                                print(f"      📝 Sample {i+1}: '{text.strip()}'")
                        except:
                            pass
            
            # Check for any forms or input fields
            print("\n📝 Looking for input elements...")
            inputs = page.locator("input, select, button")
            print(f"   Found {inputs.count()} input elements")
            
            # Look for any booking-related text on the page
            print("\n📄 Checking page content for booking keywords...")
            page_text = page.inner_text("body").lower()
            
            keywords = ["book", "reserve", "available", "select", "time", "court"]
            for keyword in keywords:
                if keyword in page_text:
                    print(f"   ✅ Found keyword: '{keyword}'")
            
            # Take a comprehensive screenshot
            page.screenshot(path="/Users/rigvedavangipurapu/Documents/Reservation Assistant/booking_analysis.png", full_page=True)
            print("\n📸 Full page screenshot saved as 'booking_analysis.png'")
            
            print("\n🕵️ Manual inspection time...")
            print("👀 Please look at the browser and identify:")
            print("   - Available time slots")
            print("   - How to select a court")
            print("   - How to pick a time")
            print("   - What happens when you click an available slot")
            print("\n⏰ Browser staying open for 30 seconds...")
            
            time.sleep(30)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    simple_booking_test()
