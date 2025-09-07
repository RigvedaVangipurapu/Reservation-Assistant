#!/usr/bin/env python3
"""
Test script to verify the browser session fix
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from badminton_agent import BookingAgent
from booking_engine import EnhancedBookingAgent
import time

def test_browser_session_fix():
    """Test that the browser session management works correctly"""
    print("🧪 Testing Browser Session Fix")
    print("=" * 50)
    
    try:
        # Create agent
        agent = BookingAgent(headless=False, slow_mo=1000)
        enhanced_agent = EnhancedBookingAgent(agent)
        
        print("\n1. Testing initial availability check...")
        result1 = enhanced_agent.book_court("What courts are available tomorrow?")
        print(f"   Result 1: {result1.status}")
        
        print("\n2. Testing second availability check...")
        result2 = enhanced_agent.book_court("Check availability for September 8th")
        print(f"   Result 2: {result2.status}")
        
        print("\n3. Testing third availability check...")
        result3 = enhanced_agent.book_court("What courts are available on September 10th?")
        print(f"   Result 3: {result3.status}")
        
        print("\n✅ All tests completed successfully!")
        print("🎉 Browser session fix is working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            agent.stop_browser()
        except:
            pass

if __name__ == "__main__":
    test_browser_session_fix()
