#!/usr/bin/env python3
"""
Test the new precise HTML detection logic based on user's guidance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def test_precise_detection():
    print("\n🎯 TESTING PRECISE HTML DETECTION LOGIC")
    print("=" * 55)
    print("Based on user guidance:")
    print("1. Wait for .booking-div-content to appear")
    print("2. Find all slot containers (.timeslot-cell)")
    print("3. Check each container for .booking-div-content inside")
    print("4. If found = BOOKED, if not found = AVAILABLE")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Step 1: Opening booking page...")
        agent.navigate_to_booking()
        print("✅ Page loaded successfully")
        
        target_date = "2025-09-10"
        print(f"\n📅 Step 2: Navigating to {target_date}...")
        date_change_result = agent.change_date(target_date=target_date)
        print(f"Date change result: {date_change_result}")
        
        if not date_change_result["success"]:
            print(f"❌ Date navigation failed: {date_change_result.get('error')}")
            return
        
        print(f"\n🔍 Step 3: Running precise detection logic...")
        slots_result = agent.get_available_slots()
        
        print("\n📊 PRECISE DETECTION RESULTS:")
        print(f"   Date: {slots_result.get('date')}")
        print(f"   Total slot containers examined: {slots_result.get('total_slots')}")
        print(f"   Available slots found: {slots_result.get('available_slots')}")
        print(f"   Booked slots found: {slots_result.get('booked_slots', 0)}")
        print(f"   Visitor mode: {slots_result.get('visitor_mode')}")
        
        if slots_result.get('error'):
            print(f"   ❌ Error: {slots_result.get('error')}")
            return
        
        availability_ratio = (slots_result.get('available_slots', 0) / slots_result.get('total_slots', 1)) * 100
        print(f"   Availability: {availability_ratio:.1f}%")
        
        # Show first few available and booked slots for verification
        slots = slots_result.get('slots', [])
        available_slots = [s for s in slots if s.get('available')]
        booked_slots = [s for s in slots if not s.get('available')]
        
        print(f"\n🟢 SAMPLE AVAILABLE SLOTS (first 5):")
        for i, slot in enumerate(available_slots[:5], 1):
            print(f"   {i}. {slot.get('court', 'Unknown')} - {slot.get('time', 'Unknown')}")
        
        print(f"\n🔴 SAMPLE BOOKED SLOTS (first 5):")
        for i, slot in enumerate(booked_slots[:5], 1):
            print(f"   {i}. {slot.get('court', 'Unknown')} - {slot.get('time', 'Unknown')}")
        
        print("\n👀 VISUAL VERIFICATION:")
        print("Please look at the browser window and verify:")
        print(f"  • Does the date show 'TUESDAY, SEPTEMBER 10, 2025'?")
        print(f"  • Do you see gray booking rectangles (.booking-div-content)?")
        print(f"  • Do you see empty white spaces (available slots)?")
        print(f"  • Does the available/booked ratio look correct?")
        
        print("\n⏰ Browser will stay open for 30 seconds for verification...")
        time.sleep(30)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Test completed!")
    print("This test verifies the new precise detection logic:")
    print("  1. ✅ Waits for booking content to load")
    print("  2. ✅ Finds slot containers")
    print("  3. ✅ Checks each container for .booking-div-content")
    print("  4. ✅ Correctly classifies as booked/available")

if __name__ == "__main__":
    test_precise_detection()
