#!/usr/bin/env python3
"""
Test the improved availability detection that can distinguish booked from available slots
"""

from badminton_agent import BookingAgent
import time

def test_improved_detection():
    """Test the improved detection with user's booked slot description"""
    
    print("🧪 TESTING IMPROVED AVAILABILITY DETECTION")
    print("=" * 50)
    print("Using new logic to detect gray rectangular booked slots")
    
    agent = BookingAgent(headless=False, slow_mo=2000)
    
    try:
        print("\n🌐 Opening booking page...")
        nav_result = agent.navigate_to_booking()
        
        if nav_result["success"]:
            print("✅ Page loaded")
            
            print("\n📊 Testing improved slot detection...")
            slots_result = agent.get_available_slots()
            
            print(f"\n📋 Detection Results:")
            print(f"   Total slots found: {slots_result.get('total_slots', 0)}")
            print(f"   Available slots: {slots_result.get('available_slots', 0)}")
            print(f"   Booked slots: {slots_result.get('total_slots', 0) - slots_result.get('available_slots', 0)}")
            print(f"   Date: {slots_result.get('date', 'Unknown')}")
            print(f"   Visitor mode: {slots_result.get('visitor_mode', False)}")
            
            if slots_result.get("slots"):
                print(f"\n📋 Sample detected slots:")
                
                available_count = 0
                booked_count = 0
                
                for i, slot in enumerate(slots_result["slots"][:15], 1):
                    status = "✅ AVAILABLE" if slot.get('available') else "🚫 BOOKED"
                    print(f"   {i:2d}. {slot.get('court', 'Unknown'):10} {slot.get('time', 'Unknown'):20} - {status}")
                    
                    if slot.get('available'):
                        available_count += 1
                    else:
                        booked_count += 1
                
                print(f"\n📊 In sample of 15 slots:")
                print(f"   Available: {available_count}")
                print(f"   Booked: {booked_count}")
                
                # Calculate ratios
                total = slots_result.get('total_slots', 1)
                available_ratio = (slots_result.get('available_slots', 0) / total) * 100
                booked_ratio = 100 - available_ratio
                
                print(f"\n📈 Overall ratios:")
                print(f"   Available: {available_ratio:.1f}%")
                print(f"   Booked: {booked_ratio:.1f}%")
                
                if available_ratio > 90:
                    print(f"   ⚠️  Warning: Very high availability ratio - may indicate detection issues")
                elif 20 <= available_ratio <= 80:
                    print(f"   ✅ Realistic availability ratio")
                else:
                    print(f"   💡 Availability ratio varies - could be accurate depending on day/time")
            
            print(f"\n🔍 Quick validation:")
            print(f"Please look at the browser and verify:")
            print(f"  • Do you see gray rectangular booked slots with time ranges?")
            print(f"  • Do the numbers above seem realistic for what you see?")
            print(f"  • Are there both available (white) and booked (gray) areas?")
            
            print(f"\n⏰ Browser will stay open for 20 seconds for manual verification...")
            time.sleep(20)
            
        else:
            print(f"❌ Failed to load page")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        agent.stop_browser()
    
    print(f"\n📝 Next step: If the ratios look realistic, we can run the availability comparison again!")

if __name__ == "__main__":
    test_improved_detection()
