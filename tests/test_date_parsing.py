#!/usr/bin/env python3
"""
Test the improved date parsing functionality
"""

from booking_engine import RequestParser

def test_date_parsing():
    """Test various date formats"""
    parser = RequestParser()
    
    test_cases = [
        "check availability for 9th september 2025",
        "book me a court on September 9th, 2025",
        "I need a court on 9/9/2025",
        "What about September 9, 2025",
        "tomorrow at 7 PM",
        "today at 9 AM",
        "book me for 2025-09-09"
    ]
    
    print("🧪 Testing Date Parsing")
    print("=" * 50)
    
    for test_case in test_cases:
        parsed = parser.parse(test_case)
        print(f"\nInput: '{test_case}'")
        print(f"  Parsed Date: {parsed.preferred_date}")
        print(f"  Parsed Time: {parsed.preferred_time}")
        print(f"  Parsed Court: {parsed.preferred_court}")

if __name__ == "__main__":
    test_date_parsing()
