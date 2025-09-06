#!/usr/bin/env python3
"""
Test specific date parsing for 'sep' abbreviation
"""

from booking_engine import RequestParser

def test_sep_parsing():
    """Test parsing of 'sep' abbreviation"""
    parser = RequestParser()
    
    test_cases = [
        "check availability on 8th sep 2025",
        "book me for 8 sep 2025", 
        "what about sep 8, 2025",
        "availability for 8th sept 2025",
        "check 8 september 2025"
    ]
    
    print("🧪 Testing 'Sep' Abbreviation Parsing")
    print("=" * 50)
    
    for test_case in test_cases:
        parsed = parser.parse(test_case)
        expected = "2025-09-08"
        result = "✅" if parsed.preferred_date == expected else "❌"
        
        print(f"\nInput: '{test_case}'")
        print(f"  Expected: {expected}")
        print(f"  Got: {parsed.preferred_date} {result}")
        print(f"  Time: {parsed.preferred_time}")
        print(f"  Court: {parsed.preferred_court}")

if __name__ == "__main__":
    test_sep_parsing()
