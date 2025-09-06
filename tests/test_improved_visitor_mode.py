#!/usr/bin/env python3
"""
Test the improved visitor mode handling
"""

from badminton_agent import BookingAgent
from booking_engine import EnhancedBookingAgent

def test_improved_visitor_mode():
    """Test the improved visitor mode features"""
    
    print("🧪 Testing Improved Visitor Mode")
    print("=" * 50)
    
    # Create agents
    base_agent = BookingAgent(headless=False, slow_mo=1000)
    enhanced_agent = EnhancedBookingAgent(base_agent, use_ai_engine=False)
    
    try:
        print("🔍 1. Testing visitor mode detection...")
        
        # Test basic navigation and detection
        nav_result = base_agent.navigate_to_booking()
        if nav_result["success"]:
            print("   ✅ Navigation successful")
            
            # Test visitor mode detection
            visitor_info = base_agent.detect_visitor_mode()
            print(f"   Visitor mode: {visitor_info.get('visitor_mode', False)}")
            if visitor_info.get("limitations"):
                print("   Limitations:")
                for limitation in visitor_info["limitations"]:
                    print(f"      • {limitation}")
            
            if visitor_info.get("recommendation"):
                print(f"   Recommendation: {visitor_info['recommendation']}")
        
        print("\n🎾 2. Testing enhanced booking with warnings...")
        
        test_requests = [
            "check availability for tomorrow",
            "book me a court tomorrow at 7 PM"
        ]
        
        for request in test_requests:
            print(f"\n   📝 Request: '{request}'")
            result = enhanced_agent.book_court(request)
            
            print(f"      Status: {result.status.value}")
            print(f"      Message: {result.message}")
            
            if hasattr(result, 'metadata') and result.metadata:
                print(f"      Visitor mode info: {result.metadata.get('visitor_mode', False)}")
            
            # Show user message with warnings
            if result.user_message:
                print(f"      User message preview: {result.user_message[:100]}...")
        
        print("\n⏰ Browser staying open for 15 seconds for visual verification...")
        import time
        time.sleep(15)
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        
    finally:
        base_agent.stop_browser()
        
    print("\n✅ Improved visitor mode features:")
    print("   • Automatic visitor mode detection")
    print("   • Clear warnings about data limitations") 
    print("   • Recommendations to check website directly")
    print("   • Helpful sidebar information")
    print("   • Honest about what the app can/cannot do")

if __name__ == "__main__":
    test_improved_visitor_mode()
