#!/usr/bin/env python3
"""
Test the Streamlit interface fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
from booking_engine import EnhancedBookingAgent, BookingStatus
import time

def test_streamlit_fix():
    print("\n🎯 TESTING STREAMLIT INTERFACE FIX")
    print("=" * 50)
    print("Testing the EnhancedBookingAgent with fixed success field handling")
    
    # Create base agent
    base_agent = BookingAgent(headless=False, slow_mo=1000)
    
    # Create enhanced agent
    enhanced_agent = EnhancedBookingAgent(base_agent, use_ai_engine=False)
    
    try:
        print("\n🌐 Testing booking request: 'What courts are available tomorrow?'")
        
        # This should now work without the 'success' field error
        result = enhanced_agent.book_court("What courts are available tomorrow?")
        
        print(f"\n📊 RESULT:")
        print(f"   Status: {result.status}")
        print(f"   Success: {result.success}")
        print(f"   Message: {result.message}")
        print(f"   User Message: {result.user_message}")
        
        if result.status == BookingStatus.FOUND_EXACT:
            print(f"   🎯 Found exact match: {result.booked_slot}")
            if result.alternatives:
                print(f"   📋 Alternatives: {len(result.alternatives)}")
        elif result.status == BookingStatus.FOUND_ALTERNATIVES:
            print(f"   📋 Found alternatives: {len(result.alternatives)}")
        elif result.status == BookingStatus.NO_SLOTS_FOUND:
            print(f"   ❌ No slots found")
        elif result.status == BookingStatus.BOOKING_FAILED:
            print(f"   ❌ Booking failed: {result.message}")
        
        print(f"\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        base_agent.stop_browser()
    
    print(f"\n🎉 STREAMLIT FIX TEST COMPLETED!")

if __name__ == "__main__":
    test_streamlit_fix()
