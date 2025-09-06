#!/usr/bin/env python3
"""
Analyze the actual slot container structure on the Skedda page
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def analyze_structure():
    print("\n🔍 ANALYZING SLOT CONTAINER STRUCTURE")
    print("=" * 55)
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        print(f"\n🔍 Analyzing page structure...")
        
        # Wait for page to load
        agent.page.wait_for_selector(".booking-div-content", timeout=10000)
        
        # Check different potential container types
        container_selectors = [
            "td",
            "div",
            "[class*='slot']",
            "[class*='time']", 
            "[class*='cell']",
            "[class*='grid']",
            "[class*='calendar']",
            "[class*='schedule']",
        ]
        
        print("\n📊 CONTAINER TYPE ANALYSIS:")
        for selector in container_selectors:
            elements = agent.page.locator(selector).filter(visible=True)
            count = elements.count()
            print(f"   {selector:20} : {count:4} elements")
        
        # Look specifically for booking content
        booking_content_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        print(f"\n🎯 BOOKED SLOTS FOUND:")
        print(f"   .booking-div-content: {booking_content_elements.count()} elements")
        
        # Sample a few booking contents
        for i in range(min(3, booking_content_elements.count())):
            element = booking_content_elements.nth(i)
            text = element.text_content() or ""
            parent_classes = ""
            try:
                parent = element.locator("xpath=..")
                if parent.count() > 0:
                    parent_classes = parent.get_attribute("class") or ""
            except:
                pass
            print(f"   Booking {i+1}: '{text[:50]}...' (parent classes: {parent_classes[:50]})")
        
        # Look for the schedule grid structure
        print(f"\n🗂️ GRID STRUCTURE ANALYSIS:")
        grid_selectors = [
            "table",
            "table td",
            "table tr",
            ".schedule-grid",
            ".calendar-grid", 
            "[class*='grid'] td",
            "[class*='grid'] div",
        ]
        
        for selector in grid_selectors:
            elements = agent.page.locator(selector).filter(visible=True)
            count = elements.count()
            if count > 0:
                print(f"   {selector:20} : {count:4} elements")
        
        # Let's look at the actual DOM structure around bookings
        print(f"\n🏗️ DOM STRUCTURE AROUND BOOKINGS:")
        if booking_content_elements.count() > 0:
            first_booking = booking_content_elements.first
            try:
                # Get parent elements
                parent = first_booking.locator("xpath=..")
                grandparent = first_booking.locator("xpath=../..")
                
                parent_tag = parent.evaluate("element => element.tagName") if parent.count() > 0 else "N/A"
                parent_class = parent.get_attribute("class") if parent.count() > 0 else "N/A"
                grandparent_tag = grandparent.evaluate("element => element.tagName") if grandparent.count() > 0 else "N/A"
                grandparent_class = grandparent.get_attribute("class") if grandparent.count() > 0 else "N/A"
                
                print(f"   Booking element hierarchy:")
                print(f"     .booking-div-content")
                print(f"       ↳ Parent: <{parent_tag}> class='{parent_class[:50]}'")
                print(f"         ↳ Grandparent: <{grandparent_tag}> class='{grandparent_class[:50]}'")
                
            except Exception as e:
                print(f"   Could not analyze DOM structure: {e}")
        
        print("\n⏰ Browser will stay open for 60 seconds for manual inspection...")
        print("Please examine the page and note:")
        print("  • What are the actual slot containers?")
        print("  • How many time slots do you see?") 
        print("  • How many courts do you see?")
        print("  • What's the total expected number of slot containers?")
        time.sleep(60)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    analyze_structure()
