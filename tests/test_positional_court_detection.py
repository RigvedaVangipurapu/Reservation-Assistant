#!/usr/bin/env python3
"""
Test positional court detection using element coordinates
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def test_positional_court_detection():
    print("\n📍 TESTING POSITIONAL COURT DETECTION")
    print("=" * 55)
    print("Logic: Group bookings by their X-coordinate (horizontal position)")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        # Wait for page to load
        agent.page.wait_for_selector(".booking-div-content", timeout=10000)
        
        print(f"\n🔍 Step 1: Get positions of all booking elements...")
        
        # Get all booking elements
        booking_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        total_bookings = booking_elements.count()
        print(f"   📊 Found {total_bookings} booking elements")
        
        bookings_with_positions = []
        
        for i in range(total_bookings):
            try:
                booking_element = booking_elements.nth(i)
                booking_text = booking_element.text_content().strip()
                
                # Get bounding box (position and size)
                bounding_box = booking_element.bounding_box()
                if bounding_box:
                    x = bounding_box['x']
                    y = bounding_box['y']
                    width = bounding_box['width']
                    height = bounding_box['height']
                    
                    bookings_with_positions.append({
                        'booking_text': booking_text,
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'element_index': i
                    })
                    
                    print(f"   📋 Booking #{i+1:2}: x={x:4.0f} y={y:4.0f} '{booking_text}'")
                else:
                    print(f"   ❌ Booking #{i+1}: Could not get position")
                    
            except Exception as e:
                print(f"   ❌ Error getting position for booking #{i+1}: {e}")
        
        print(f"\n🔍 Step 2: Group bookings by X-coordinate (court columns)...")
        
        # Sort by X coordinate to find court boundaries
        bookings_with_positions.sort(key=lambda x: x['x'])
        
        # Find distinct X positions (court columns)
        x_positions = []
        tolerance = 10  # pixels tolerance for grouping
        
        for booking in bookings_with_positions:
            x = booking['x']
            # Check if this X position is close to an existing one
            found_group = False
            for existing_x in x_positions:
                if abs(x - existing_x) <= tolerance:
                    found_group = True
                    break
            
            if not found_group:
                x_positions.append(x)
        
        x_positions.sort()
        print(f"   📊 Found {len(x_positions)} distinct X positions (court columns)")
        
        for i, x_pos in enumerate(x_positions):
            print(f"     Column {i+1}: X ≈ {x_pos:.0f}")
        
        print(f"\n🔍 Step 3: Assign courts based on X-position...")
        
        # Assign each booking to a court based on its X position
        for booking in bookings_with_positions:
            x = booking['x']
            
            # Find the closest X position
            closest_court = 1
            min_distance = float('inf')
            
            for i, x_pos in enumerate(x_positions):
                distance = abs(x - x_pos)
                if distance < min_distance:
                    min_distance = distance
                    closest_court = i + 1
            
            booking['court'] = f"Court #{closest_court}"
        
        # Sort back to original order
        bookings_with_positions.sort(key=lambda x: x['element_index'])
        
        print(f"\n📊 RESULTS BY ORIGINAL ORDER:")
        for booking in bookings_with_positions:
            print(f"   Booking #{booking['element_index']+1:2}: {booking['court']:8} x={booking['x']:4.0f} '{booking['booking_text']}'")
        
        print(f"\n📊 RESULTS SUMMARY:")
        
        # Group by court
        court_groups = {}
        for booking in bookings_with_positions:
            court = booking['court']
            if court not in court_groups:
                court_groups[court] = []
            court_groups[court].append(booking)
        
        total_courts_found = len(court_groups)
        print(f"   Total courts detected: {total_courts_found}")
        
        for court_num in range(1, total_courts_found + 1):
            court_name = f"Court #{court_num}"
            if court_name in court_groups:
                bookings = court_groups[court_name]
                print(f"\n   {court_name}: {len(bookings)} bookings")
                
                # Show X position range for this court
                x_positions_court = [b['x'] for b in bookings]
                min_x = min(x_positions_court)
                max_x = max(x_positions_court)
                print(f"     X position range: {min_x:.0f} - {max_x:.0f}")
                
                # Show sample bookings
                for booking in bookings[:3]:
                    print(f"     - {booking['booking_text']}")
                if len(bookings) > 3:
                    print(f"     - ... and {len(bookings) - 3} more")
        
        print(f"\n🔍 Step 4: Verify the results make sense...")
        
        if total_courts_found == 8:
            print(f"   ✅ PERFECT: Detected exactly 8 courts as expected!")
        elif total_courts_found < 8:
            print(f"   ⚠️ CAUTION: Only detected {total_courts_found} courts, expected 8")
            print(f"      Some courts might not have bookings, or tolerance needs adjustment")
        else:
            print(f"   ❌ ERROR: Detected {total_courts_found} courts, more than expected 8")
            print(f"      Tolerance might be too strict, grouping similar positions separately")
        
        # Show the X-coordinate distribution
        print(f"\n📊 X-COORDINATE DISTRIBUTION:")
        all_x = [b['x'] for b in bookings_with_positions]
        min_x_overall = min(all_x)
        max_x_overall = max(all_x)
        print(f"   Overall X range: {min_x_overall:.0f} - {max_x_overall:.0f}")
        print(f"   Court width estimate: {(max_x_overall - min_x_overall) / max(1, total_courts_found - 1):.0f} pixels")
        
        print(f"\n👀 MANUAL VERIFICATION:")
        print("Please look at the browser and verify:")
        print("  • Do the court assignments look correct?")
        print("  • Are bookings properly grouped by court column?")
        print("  • Does each court have a reasonable number of bookings?")
        
        print("\n⏰ Browser staying open for 45 seconds for verification...")
        time.sleep(45)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Positional court detection test completed!")
    print("If this works well, we can integrate this logic into the main agent.")

if __name__ == "__main__":
    test_positional_court_detection()
