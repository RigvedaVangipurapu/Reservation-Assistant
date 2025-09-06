#!/usr/bin/env python3
"""
Test sequential court detection using time order logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time
from datetime import datetime

def test_sequential_court_detection():
    print("\n🔄 TESTING SEQUENTIAL COURT DETECTION")
    print("=" * 55)
    print("Logic: When time goes backwards, we've moved to a new court")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        # Wait for page to load
        agent.page.wait_for_selector(".booking-div-content", timeout=10000)
        
        print(f"\n🔍 Step 1: Get all booking elements in DOM order...")
        
        # Get all booking elements (they should be in DOM order)
        booking_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        total_bookings = booking_elements.count()
        print(f"   📊 Found {total_bookings} booking elements")
        
        print(f"\n🔍 Step 2: Extract times and detect court boundaries...")
        
        def parse_time(time_str):
            """Parse time string to datetime for comparison"""
            try:
                # Extract start time from "X:XX AM/PM–Y:YY AM/PM" format
                import re
                time_pattern = r'(\d{1,2}:\d{2}\s*[AP]M)'
                match = re.search(time_pattern, time_str)
                if match:
                    time_part = match.group(1).strip()
                    return datetime.strptime(time_part, "%I:%M %p")
                return None
            except:
                return None
        
        bookings_with_courts = []
        current_court = 1
        previous_time = None
        
        print(f"\n📋 ANALYZING BOOKING SEQUENCE:")
        
        for i in range(total_bookings):
            try:
                booking_element = booking_elements.nth(i)
                booking_text = booking_element.text_content().strip()
                
                # Parse the start time
                current_time = parse_time(booking_text)
                
                # Detect court boundary
                if previous_time is not None and current_time is not None:
                    # If current time is earlier than previous time, we've moved to next court
                    if current_time < previous_time:
                        current_court += 1
                        print(f"   🔄 COURT BOUNDARY DETECTED: Moving to Court #{current_court}")
                        print(f"      Previous: {previous_time.strftime('%I:%M %p')} → Current: {current_time.strftime('%I:%M %p')}")
                
                court_name = f"Court #{current_court}"
                
                bookings_with_courts.append({
                    'booking_text': booking_text,
                    'court': court_name,
                    'start_time': current_time,
                    'element_index': i
                })
                
                time_str = current_time.strftime('%I:%M %p') if current_time else 'Unknown'
                print(f"   📋 Booking #{i+1:2}: {court_name} - {time_str} - '{booking_text}'")
                
                previous_time = current_time
                
            except Exception as e:
                print(f"   ❌ Error processing booking #{i+1}: {e}")
                # Still add it with unknown time
                bookings_with_courts.append({
                    'booking_text': booking_text,
                    'court': f"Court #{current_court}",
                    'start_time': None,
                    'element_index': i
                })
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Total bookings: {len(bookings_with_courts)}")
        print(f"   Courts detected: {current_court}")
        
        # Group by court
        court_groups = {}
        for booking in bookings_with_courts:
            court = booking['court']
            if court not in court_groups:
                court_groups[court] = []
            court_groups[court].append(booking)
        
        for court_num in range(1, current_court + 1):
            court_name = f"Court #{court_num}"
            if court_name in court_groups:
                bookings = court_groups[court_name]
                print(f"\n   {court_name}: {len(bookings)} bookings")
                
                # Show times in order to verify they're chronological within each court
                times = []
                for booking in bookings:
                    if booking['start_time']:
                        times.append(booking['start_time'].strftime('%I:%M %p'))
                    else:
                        times.append('Unknown')
                
                print(f"     Times: {' → '.join(times)}")
                
                # Show sample bookings
                for booking in bookings[:3]:
                    print(f"     - {booking['booking_text']}")
                if len(bookings) > 3:
                    print(f"     - ... and {len(bookings) - 3} more")
        
        print(f"\n🔍 Step 3: Verify the logic makes sense...")
        
        if current_court == 8:
            print(f"   ✅ PERFECT: Detected exactly 8 courts as expected!")
        elif current_court < 8:
            print(f"   ⚠️ CAUTION: Only detected {current_court} courts, expected 8")
            print(f"      This might mean some courts have no bookings")
        else:
            print(f"   ❌ ERROR: Detected {current_court} courts, more than expected 8")
            print(f"      The time-order logic might need refinement")
        
        # Verify times are chronological within each court
        print(f"\n🔍 Step 4: Verify times are chronological within courts...")
        
        for court_num in range(1, min(current_court + 1, 4)):  # Check first 3 courts
            court_name = f"Court #{court_num}"
            if court_name in court_groups:
                bookings = court_groups[court_name]
                times_with_data = [(b['start_time'], b['booking_text']) for b in bookings if b['start_time']]
                
                print(f"   {court_name}:")
                is_chronological = True
                for i in range(1, len(times_with_data)):
                    prev_time, prev_text = times_with_data[i-1]
                    curr_time, curr_text = times_with_data[i]
                    
                    if curr_time < prev_time:
                        print(f"     ❌ NOT CHRONOLOGICAL: {prev_time.strftime('%I:%M %p')} → {curr_time.strftime('%I:%M %p')}")
                        is_chronological = False
                    else:
                        print(f"     ✅ {prev_time.strftime('%I:%M %p')} → {curr_time.strftime('%I:%M %p')}")
                
                if is_chronological:
                    print(f"     ✅ {court_name} times are chronological!")
                else:
                    print(f"     ❌ {court_name} times are NOT chronological - logic needs adjustment")
        
        print(f"\n👀 MANUAL VERIFICATION:")
        print("Please look at the browser and verify:")
        print("  • Do the court assignments look correct?")
        print("  • Are bookings in each court grouped together?")
        print("  • Do the time progressions make sense?")
        
        print("\n⏰ Browser staying open for 45 seconds for verification...")
        time.sleep(45)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Sequential court detection test completed!")
    print("If this works well, we can integrate this logic into the main agent.")

if __name__ == "__main__":
    test_sequential_court_detection()
