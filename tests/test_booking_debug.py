#!/usr/bin/env python3
"""
Debug the booking engine - test individual components
"""

from booking_engine import RequestParser, TimeSlot, RuleBasedDecisionEngine, BookingRequest, BookingStrategy
from datetime import datetime

def test_request_parsing():
    """Test the request parser"""
    parser = RequestParser()
    
    test_requests = [
        "Book me a court tomorrow at 7 PM",
        "I need Court #2 today at 9 AM", 
        "Find me any available court this afternoon around 3 PM"
    ]
    
    print("🧪 Testing Request Parsing")
    for request in test_requests:
        parsed = parser.parse(request)
        print(f"\nRequest: '{request}'")
        print(f"  Date: {parsed.preferred_date}")
        print(f"  Time: {parsed.preferred_time}")
        print(f"  Court: {parsed.preferred_court}")

def test_time_matching():
    """Test time slot matching logic"""
    print("\n🧪 Testing Time Slot Matching")
    
    # Create sample time slots (like what we get from the website)
    sample_slots = [
        TimeSlot(
            court="Court #1",
            start_time="9:00 AM",
            end_time="11:00 AM", 
            date="2025-09-06",
            available=True
        ),
        TimeSlot(
            court="Court #2",
            start_time="6:00 PM",
            end_time="8:00 PM",
            date="2025-09-06", 
            available=True
        ),
        TimeSlot(
            court="Court #3",
            start_time="7:00 PM",
            end_time="9:00 PM",
            date="2025-09-06",
            available=True
        )
    ]
    
    # Test time matching
    engine = RuleBasedDecisionEngine()
    
    test_times = ["7:00 PM", "9:00 AM", "6:30 PM"]
    
    for test_time in test_times:
        print(f"\nLooking for: {test_time}")
        for slot in sample_slots:
            score = engine._calculate_time_score(slot, test_time, 60)  # 60 min flexibility
            contains = slot.contains_time(test_time)
            print(f"  {slot.court} {slot.time_range}: score={score:.2f}, contains={contains}")

def test_decision_engine():
    """Test the decision engine"""
    print("\n🧪 Testing Decision Engine")
    
    # Create a request
    request = BookingRequest(
        raw_request="Book me a court tomorrow at 7 PM",
        preferred_date="2025-09-06",
        preferred_time="7:00 PM",
        strategy=BookingStrategy.SMART_FALLBACK
    )
    
    # Sample available slots
    available_slots = [
        TimeSlot("Court #1", "9:00 AM", "11:00 AM", "2025-09-06", True),
        TimeSlot("Court #2", "6:00 PM", "8:00 PM", "2025-09-06", True),
        TimeSlot("Court #3", "7:00 PM", "9:00 PM", "2025-09-06", True),
        TimeSlot("Court #4", "2:00 PM", "4:00 PM", "2025-09-06", True),
    ]
    
    engine = RuleBasedDecisionEngine()
    best_slots = engine.find_best_slots(request, available_slots)
    
    print(f"Request: {request.preferred_time} on {request.preferred_date}")
    print(f"Best matches found: {len(best_slots)}")
    
    for i, slot in enumerate(best_slots):
        score = engine._calculate_time_score(slot, request.preferred_time, 60)
        print(f"  {i+1}. {slot.court} {slot.time_range} (score: {score:.2f})")

if __name__ == "__main__":
    test_request_parsing()
    test_time_matching()
    test_decision_engine()
