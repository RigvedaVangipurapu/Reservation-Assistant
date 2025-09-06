#!/usr/bin/env python3
"""
Simple test of the complete booking system
"""

from badminton_agent import BookingAgent
from booking_engine import EnhancedBookingAgent

def test_simple_booking():
    """Test a simple booking request"""
    
    print("🧪 Testing Simple Booking Request")
    
    # Create base agent
    base_agent = BookingAgent(headless=False, slow_mo=1000)
    
    # Create enhanced agent
    enhanced_agent = EnhancedBookingAgent(base_agent, use_ai_engine=False)  # Use rule-based for consistency
    
    # Simple test request
    request = "Book me any available court tomorrow around 9 AM"
    
    print(f"🎯 Request: {request}")
    
    try:
        result = enhanced_agent.book_court(request)
        
        print(f"\n📊 Result:")
        print(f"   Status: {result.status.value}")
        print(f"   Success: {result.success}")
        print(f"   Message: {result.message}")
        print(f"   User Message: {result.user_message}")
        
        if result.booked_slot:
            slot = result.booked_slot
            print(f"   Booked Slot: {slot.court} at {slot.time_range} on {slot.date}")
        
        if result.alternatives:
            print(f"   Alternatives: {len(result.alternatives)} options")
            for i, alt in enumerate(result.alternatives[:3]):
                print(f"      {i+1}. {alt.court} at {alt.time_range}")
        
        # Keep browser open for inspection
        print("\n🔍 Browser staying open for 15 seconds for inspection...")
        import time
        time.sleep(15)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        base_agent.stop_browser()

if __name__ == "__main__":
    test_simple_booking()
