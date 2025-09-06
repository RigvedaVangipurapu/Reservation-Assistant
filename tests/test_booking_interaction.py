#!/usr/bin/env python3
"""
Test script to interact with the Skedda booking interface and understand the booking flow
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

def test_booking_interaction():
    """Test interaction with the Skedda booking interface"""
    
    with sync_playwright() as p:
        # Launch browser in visible mode (as chosen)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        # Set longer timeout
        page.set_default_timeout(60000)
        
        try:
            print("🌐 Loading OC Badminton booking page...")
            page.goto("https://ocbadminton.skedda.com/booking")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            
            print("✅ Page loaded successfully")
            
            # Test 1: Check different view modes
            print("\n📊 Testing view modes...")
            
            # Try Day view (use more specific selector)
            day_button = page.locator("button.dropdown-item:has-text('Day')")
            if day_button.count() > 0:
                print("🔘 Clicking Day view...")
                day_button.first.click()
                time.sleep(2)
            
            # Try Grid view  
            grid_button = page.locator("button.dropdown-item:has-text('Grid')")
            if grid_button.count() > 0:
                print("🔘 Clicking Grid view...")
                grid_button.first.click()
                time.sleep(2)
            
            # Test 2: Check date navigation
            print("\n📅 Testing date navigation...")
            
            # Look for date picker
            date_inputs = page.locator("input[type='date']")
            if date_inputs.count() > 0:
                print("📆 Found date input field")
                # Try to set tomorrow's date
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                date_inputs.first.fill(tomorrow)
                print(f"📅 Set date to: {tomorrow}")
                time.sleep(3)
            
            # Test 3: Look for available time slots
            print("\n🕐 Looking for available time slots...")
            
            # Look for clickable time slots (these might have different selectors)
            time_slots = page.locator("[class*='slot'], [class*='time'], [class*='available']")
            slot_count = time_slots.count()
            print(f"🎯 Found {slot_count} potential time slot elements")
            
            if slot_count > 0:
                # Get text content of first few slots to understand structure
                for i in range(min(5, slot_count)):
                    try:
                        slot_text = time_slots.nth(i).text_content()
                        if slot_text and slot_text.strip():
                            print(f"   📍 Slot {i+1}: {slot_text.strip()}")
                    except Exception as e:
                        print(f"   ❌ Could not read slot {i+1}: {e}")
            
            # Test 4: Look for court information
            print("\n🏸 Looking for court information...")
            
            # Look for court labels
            court_elements = page.locator("[class*='court'], text=/Court.*#/")
            court_count = court_elements.count()
            print(f"🎾 Found {court_count} court elements")
            
            if court_count > 0:
                for i in range(min(3, court_count)):
                    try:
                        court_text = court_elements.nth(i).text_content()
                        if court_text and court_text.strip():
                            print(f"   🏸 Court {i+1}: {court_text.strip()}")
                    except Exception as e:
                        print(f"   ❌ Could not read court {i+1}: {e}")
            
            # Test 5: Try clicking on an available slot (if any)
            print("\n🖱️ Testing slot interaction...")
            
            # Look for specifically available/bookable slots
            available_slots = page.locator("[class*='available']:not([class*='booked']):not([class*='unavailable'])")
            available_count = available_slots.count()
            print(f"✅ Found {available_count} potentially available slots")
            
            if available_count > 0:
                print("🖱️ Trying to click on first available slot...")
                try:
                    available_slots.first.click()
                    time.sleep(3)
                    
                    # Check if any modal or booking form appeared
                    modals = page.locator("[class*='modal'], [class*='dialog'], [class*='popup']")
                    if modals.count() > 0:
                        print("🪟 Booking modal/dialog appeared!")
                        modal_text = modals.first.text_content()
                        print(f"📝 Modal content preview: {modal_text[:200]}...")
                    else:
                        print("❓ No modal appeared - checking page changes...")
                        
                except Exception as e:
                    print(f"❌ Could not click slot: {e}")
            
            # Take final screenshot
            page.screenshot(path="/Users/rigvedavangipurapu/Documents/Reservation Assistant/booking_interface_test.png")
            print("\n📸 Screenshot saved as 'booking_interface_test.png'")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 20 seconds for detailed inspection...")
            print("👀 Please manually explore the interface and note any booking patterns")
            time.sleep(20)
            
        except Exception as e:
            print(f"❌ Error during booking interaction test: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_booking_interaction()
