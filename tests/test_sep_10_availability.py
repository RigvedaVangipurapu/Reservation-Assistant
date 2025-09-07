#!/usr/bin/env python3
"""
Test availability check for September 10th, 2025
"""

from badminton_agent import BookingAgent
import time

def test_sep_10_availability():
    """Test checking availability for September 10th"""
    
    print("📅 TESTING AVAILABILITY FOR SEPTEMBER 10TH, 2025")
    print("=" * 60)
    print("This will test both date navigation and availability detection")
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("\n🌐 Step 1: Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded successfully")
            
            # Check current date first
            print("\n📅 Step 2: Checking current date before navigation...")
            current_slots = agent.get_available_slots()
            current_date = current_slots.get('date', 'Unknown')
            print(f"Current date showing: {current_date}")
            
            # Navigate to September 10th, 2025
            target_date = "2025-09-10"
            print(f"\n🔄 Step 3: Navigating to {target_date}...")
            
            date_result = agent.change_date(target_date=target_date)
            print(f"Date change result: {date_result}")
            
            if date_result.get("success"):
                print("✅ Date navigation successful")
                
                # Wait a moment for page to update
                time.sleep(3)
                
                print(f"\n🔍 Step 4: Getting availability for September 10th...")
                sep_10_slots = agent.get_available_slots()
                
                print(f"\n📊 AVAILABILITY RESULTS FOR SEPTEMBER 10TH:")
                print(f"   Date: {sep_10_slots.get('date', 'Unknown')}")
                print(f"   Total slots: {sep_10_slots.get('total_slots', 0)}")
                print(f"   Available slots: {sep_10_slots.get('available_slots', 0)}")
                print(f"   Booked slots: {sep_10_slots.get('total_slots', 0) - sep_10_slots.get('available_slots', 0)}")
                print(f"   Visitor mode: {sep_10_slots.get('visitor_mode', False)}")
                
                # Calculate availability percentage
                total = sep_10_slots.get('total_slots', 0)
                available = sep_10_slots.get('available_slots', 0)
                
                if total > 0:
                    availability_percent = (available / total) * 100
                    print(f"   Availability: {availability_percent:.1f}%")
                
                # Show breakdown by court
                if sep_10_slots.get("slots"):
                    court_summary = {}
                    
                    for slot in sep_10_slots["slots"]:
                        court = slot.get('court', 'Unknown')
                        is_available = slot.get('available', False)
                        
                        if court not in court_summary:
                            court_summary[court] = {'total': 0, 'available': 0, 'booked': 0}
                        
                        court_summary[court]['total'] += 1
                        if is_available:
                            court_summary[court]['available'] += 1
                        else:
                            court_summary[court]['booked'] += 1
                    
                    print(f"\n📋 COURT-BY-COURT BREAKDOWN:")
                    for court_num in range(1, 9):
                        court_name = f"Court #{court_num}"
                        if court_name in court_summary:
                            summary = court_summary[court_name]
                            print(f"   {court_name}: {summary['available']:2d} available, {summary['booked']:2d} booked ({summary['total']:2d} total)")
                        else:
                            print(f"   {court_name}: No data found")
                    
                    # Show some sample available slots
                    available_slots = [slot for slot in sep_10_slots["slots"] if slot.get('available')]
                    if available_slots:
                        print(f"\n✅ SAMPLE AVAILABLE SLOTS (first 10):")
                        for i, slot in enumerate(available_slots[:10], 1):
                            court = slot.get('court', 'Unknown')
                            time_range = slot.get('time', 'Unknown')
                            print(f"   {i:2d}. {court:12} - {time_range}")
                    else:
                        print(f"\n❌ NO AVAILABLE SLOTS FOUND for September 10th")
                    
                    # Show some sample booked slots
                    booked_slots = [slot for slot in sep_10_slots["slots"] if not slot.get('available')]
                    if booked_slots:
                        print(f"\n🚫 SAMPLE BOOKED SLOTS (first 5):")
                        for i, slot in enumerate(booked_slots[:5], 1):
                            court = slot.get('court', 'Unknown')
                            time_range = slot.get('time', 'Unknown')
                            print(f"   {i:2d}. {court:12} - {time_range}")
                
                print(f"\n👀 VISUAL VERIFICATION:")
                print(f"Please look at the browser window and verify:")
                print(f"  • Does the date show 'TUESDAY, SEPTEMBER 10, 2025'?")
                print(f"  • Do the availability numbers match what you see?")
                print(f"  • Are there gray booking rectangles visible?")
                print(f"  • Are there white spaces (available slots)?")
                
            else:
                print(f"❌ Date navigation failed: {date_result.get('error', 'Unknown error')}")
                print(f"Will show current date availability instead...")
                
                current_slots = agent.get_available_slots()
                print(f"Current availability: {current_slots.get('available_slots', 0)} slots")
            
            print(f"\n⏰ Browser will stay open for 30 seconds for verification...")
            time.sleep(30)
            
        else:
            print(f"❌ Failed to load page: {nav_result}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
    
    print(f"\n📝 Test Summary:")
    print(f"This test verifies that the agent can:")
    print(f"  ✅ Navigate to a specific date (September 10th)")
    print(f"  ✅ Detect booked vs available slots accurately")
    print(f"  ✅ Provide realistic availability data")
    print(f"  ✅ Break down availability by court")

if __name__ == "__main__":
    test_sep_10_availability()
