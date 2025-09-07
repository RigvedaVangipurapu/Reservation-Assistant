#!/usr/bin/env python3
"""
Test the comprehensive webpage understanding update
"""

from badminton_agent import BookingAgent
import time

def test_comprehensive_update():
    """Test with the comprehensive webpage understanding"""
    
    print("🎯 TESTING COMPREHENSIVE WEBPAGE UNDERSTANDING")
    print("=" * 55)
    print("Based on detailed webpage description:")
    print("• Grid view with Courts #1-#8 (columns)")
    print("• Time 8:00 AM - 9:00 PM (rows)")  
    print("• Gray boxes = booked slots")
    print("• White spaces = available slots")
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("\n🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded")
            
            print("\n📊 Testing comprehensive slot detection...")
            slots_result = agent.get_available_slots()
            
            print(f"\n📋 Comprehensive Detection Results:")
            print(f"   Total slots found: {slots_result.get('total_slots', 0)}")
            print(f"   Available slots: {slots_result.get('available_slots', 0)}")
            print(f"   Booked slots: {slots_result.get('total_slots', 0) - slots_result.get('available_slots', 0)}")
            print(f"   Date: {slots_result.get('date', 'Unknown')}")
            print(f"   Visitor mode: {slots_result.get('visitor_mode', False)}")
            
            # Calculate coverage across courts
            court_coverage = {}
            available_by_court = {}
            
            if slots_result.get("slots"):
                for slot in slots_result["slots"]:
                    court = slot.get('court', 'Unknown')
                    available = slot.get('available', False)
                    
                    if court not in court_coverage:
                        court_coverage[court] = 0
                        available_by_court[court] = 0
                    
                    court_coverage[court] += 1
                    if available:
                        available_by_court[court] += 1
                
                print(f"\n📊 Court Coverage Analysis:")
                for court_num in range(1, 9):  # Courts #1 to #8
                    court_name = f"Court #{court_num}"
                    total = court_coverage.get(court_name, 0)
                    available = available_by_court.get(court_name, 0)
                    booked = total - available
                    
                    if total > 0:
                        print(f"   {court_name:12}: {total:3d} total ({available:3d} avail, {booked:3d} booked)")
                    else:
                        print(f"   {court_name:12}: Not detected")
                
                print(f"\n📋 Sample slots (first 10):")
                for i, slot in enumerate(slots_result["slots"][:10], 1):
                    status = "✅ AVAIL" if slot.get('available') else "🚫 BOOKED"
                    print(f"   {i:2d}. {slot.get('court', 'Unknown'):12} {slot.get('time', 'Unknown'):20} - {status}")
                
                # Check for realistic patterns
                total_slots = slots_result.get('total_slots', 0)
                available_slots = slots_result.get('available_slots', 0)
                
                if total_slots > 0:
                    availability_ratio = (available_slots / total_slots) * 100
                    print(f"\n📈 Availability Analysis:")
                    print(f"   Availability ratio: {availability_ratio:.1f}%")
                    
                    if 10 <= availability_ratio <= 70:
                        print(f"   ✅ Realistic availability ratio for a busy booking system")
                    elif availability_ratio > 90:
                        print(f"   ⚠️  Very high availability - may indicate detection issues")
                    else:
                        print(f"   💡 Low availability - could be accurate for a busy day")
                
                # Look for court distribution
                detected_courts = len(court_coverage)
                print(f"   Detected courts: {detected_courts}/8")
                
                if detected_courts >= 7:
                    print(f"   ✅ Good court coverage")
                elif detected_courts >= 5:
                    print(f"   ⚠️  Partial court coverage")
                else:
                    print(f"   ❌ Poor court coverage")
            
            print(f"\n👀 Visual Verification:")
            print(f"Please look at the browser and verify:")
            print(f"  • Is this the Grid view with time rows and court columns?")
            print(f"  • Do you see Courts #1 through #8 across the top?")
            print(f"  • Are there gray booking rectangles in the grid?")
            print(f"  • Do the numbers above match what you visually see?")
            
            print(f"\n⏰ Browser will stay open for 25 seconds for verification...")
            time.sleep(25)
            
        else:
            print(f"❌ Failed to load page")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
    
    print(f"\n📝 Summary:")
    print(f"With the comprehensive webpage understanding, the agent should now:")
    print(f"  ✅ Recognize all 8 courts")
    print(f"  ✅ Properly detect booked vs available slots") 
    print(f"  ✅ Generate realistic availability ratios")
    print(f"  ✅ Better match what you visually see")

if __name__ == "__main__":
    test_comprehensive_update()
