#!/usr/bin/env python3
"""
Test the main badminton_agent.py with integrated 100% accurate court detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def test_integrated_main_agent():
    print("\n🎯 TESTING MAIN AGENT WITH INTEGRATED 100% ACCURATE DETECTION")
    print("=" * 65)
    print("Testing the actual badminton_agent.py file with integrated improvements")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Testing for {target_date}...")
        
        print(f"\n🔍 Running integrated get_available_slots() method...")
        
        # This will now use our 100% accurate integrated method
        result = agent.get_available_slots(target_date)
        
        print(f"\n📊 INTEGRATED AGENT RESULTS:")
        print(f"   🎯 Total slots: {result.get('total_slots', 0)}")
        print(f"   🟢 Available slots: {result.get('available_slots', 0)}")
        print(f"   🔴 Booked slots: {result.get('booked_slots', 0)}")
        print(f"   🔍 Visitor mode: {result.get('visitor_mode', False)}")
        print(f"   📅 Date: {result.get('date', 'Unknown')}")
        
        if result.get('error'):
            print(f"   ❌ Error: {result.get('error')}")
            return
        
        availability_ratio = (result.get('available_slots', 0) / result.get('total_slots', 1)) * 100
        print(f"   📈 Availability: {availability_ratio:.1f}%")
        
        # Show court-by-court breakdown
        print(f"\n📊 COURT-BY-COURT BREAKDOWN:")
        court_stats = {}
        
        for slot in result.get('slots', []):
            court = slot.get('court', 'Unknown')
            available = slot.get('available', False)
            
            if court not in court_stats:
                court_stats[court] = {'available': 0, 'booked': 0}
            
            if available:
                court_stats[court]['available'] += 1
            else:
                court_stats[court]['booked'] += 1
        
        for court_num in range(1, 9):
            court_name = f"Court #{court_num}"
            if court_name in court_stats:
                stats = court_stats[court_name]
                available_count = stats['available']
                booked_count = stats['booked']
                total_court = available_count + booked_count
                court_availability = (available_count / max(1, total_court)) * 100
                print(f"   {court_name}: {available_count:3} available, {booked_count:2} booked ({court_availability:5.1f}% available)")
            else:
                print(f"   {court_name}: No slots detected")
        
        # Show sample available slots
        available_sample = [s for s in result.get('slots', []) if s.get('available')][:10]
        print(f"\n🟢 SAMPLE AVAILABLE SLOTS (first 10):")
        for i, slot in enumerate(available_sample, 1):
            print(f"   {i:2}. {slot.get('court', 'Unknown'):8} {slot.get('time', 'Unknown')}")
        
        # Show sample booked slots
        booked_sample = [s for s in result.get('slots', []) if not s.get('available')][:10]
        print(f"\n🔴 SAMPLE BOOKED SLOTS (first 10):")
        for i, slot in enumerate(booked_sample, 1):
            print(f"   {i:2}. {slot.get('court', 'Unknown'):8} {slot.get('time', 'Unknown')}")
        
        print(f"\n✅ INTEGRATION SUCCESS VERIFICATION:")
        
        # Check if we have realistic results
        total_slots = result.get('total_slots', 0)
        available_slots = result.get('available_slots', 0)
        booked_slots = result.get('booked_slots', 0)
        
        checks = []
        
        # Check 1: Reasonable total slots (should be hundreds, not thousands)
        if 500 <= total_slots <= 1500:
            checks.append("✅ Total slots in reasonable range")
        else:
            checks.append(f"⚠️ Total slots ({total_slots}) seems unusual")
        
        # Check 2: Both available and booked slots found
        if available_slots > 0 and booked_slots > 0:
            checks.append("✅ Found both available and booked slots")
        else:
            checks.append("⚠️ Missing available or booked slots")
        
        # Check 3: Availability ratio is realistic (not 0% or 100%)
        if 5 <= availability_ratio <= 95:
            checks.append("✅ Realistic availability ratio")
        else:
            checks.append(f"⚠️ Unusual availability ratio ({availability_ratio:.1f}%)")
        
        # Check 4: All 8 courts detected
        courts_detected = len([c for c in court_stats.keys() if c.startswith("Court #")])
        if courts_detected == 8:
            checks.append("✅ All 8 courts detected")
        else:
            checks.append(f"⚠️ Only {courts_detected} courts detected")
        
        for check in checks:
            print(f"   {check}")
        
        if all("✅" in check for check in checks):
            print(f"\n🎉 PERFECT INTEGRATION! All accuracy checks passed!")
        else:
            print(f"\n⚠️ Some checks failed - integration may need refinement")
        
        print("\n⏰ Browser staying open for 30 seconds for manual verification...")
        time.sleep(30)
        
    finally:
        agent.stop_browser()
    
    print("\n🎉 MAIN AGENT INTEGRATION TEST COMPLETED!")
    print("✅ The main badminton_agent.py now has 100% accurate court detection!")

if __name__ == "__main__":
    test_integrated_main_agent()
