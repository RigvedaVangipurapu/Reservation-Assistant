#!/usr/bin/env python3
"""
Simple test of the booking agent - just basic functionality
"""

from badminton_agent import BookingAgent

def test_basic_functionality():
    """Test basic agent functionality step by step"""
    
    print("🧪 Testing Basic Agent Functionality")
    
    # Create agent
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        # Test 1: Navigation
        print("\n1️⃣ Testing navigation...")
        nav_result = agent.navigate_to_booking()
        print(f"   Result: {nav_result['success']} - {nav_result['message']}")
        
        if not nav_result["success"]:
            return
        
        # Test 2: Get page state
        print("\n2️⃣ Testing page state...")
        state_result = agent.get_current_page_state()
        print(f"   Result: {state_result['success']} - Found {state_result.get('courts_found', 0)} courts")
        print(f"   Current date: {state_result.get('current_date', 'Unknown')}")
        
        # Test 3: Get available slots
        print("\n3️⃣ Testing slot availability...")
        slots_result = agent.get_available_slots()
        print(f"   Result: {slots_result['success']} - {slots_result.get('message', 'No message')}")
        
        if slots_result["success"] and slots_result.get("slots"):
            print("   📋 Sample available slots:")
            for i, slot in enumerate(slots_result["slots"][:3]):  # Show first 3
                print(f"      {i+1}. {slot['court']} - {slot['time']} ({'Available' if slot['available'] else 'Booked'})")
        
        # Test 4: Date change
        print("\n4️⃣ Testing date change...")
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        date_result = agent.change_date(target_date=tomorrow)
        print(f"   Result: {date_result['success']} - {date_result.get('message', 'No message')}")
        
        # Test 5: Get slots for new date
        if date_result["success"]:
            print("\n5️⃣ Testing slots after date change...")
            new_slots_result = agent.get_available_slots()
            print(f"   Result: {new_slots_result['success']} - {new_slots_result.get('message', 'No message')}")
            
            if new_slots_result["success"] and new_slots_result.get("slots"):
                print("   📋 Sample slots for tomorrow:")
                for i, slot in enumerate(new_slots_result["slots"][:3]):
                    print(f"      {i+1}. {slot['court']} - {slot['time']} ({'Available' if slot['available'] else 'Booked'})")
        
        print("\n✅ Basic functionality test completed!")
        print("🔍 Browser will stay open for 10 seconds for inspection...")
        import time
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
    finally:
        agent.stop_browser()

if __name__ == "__main__":
    test_basic_functionality()
