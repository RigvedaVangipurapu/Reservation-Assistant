#!/usr/bin/env python3
"""
Analyze how to properly detect which court each booking element belongs to
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def analyze_court_detection():
    print("\n🔍 ANALYZING COURT DETECTION METHODS")
    print("=" * 55)
    print("Goal: Figure out how to map each .booking-div-content to its correct court")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        print(f"\n🔍 Step 1: Find all booking elements...")
        
        # Wait for page to load
        agent.page.wait_for_selector(".booking-div-content", timeout=10000)
        
        # Find all booking elements
        booking_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        total_count = booking_elements.count()
        print(f"   📊 Found {total_count} booking elements")
        
        print(f"\n🔍 Step 2: Analyze DOM structure around each booking...")
        
        # Analyze first few elements to understand the structure
        for i in range(min(5, total_count)):
            element = booking_elements.nth(i)
            text = element.text_content() or ""
            
            print(f"\n📋 BOOKING ELEMENT #{i+1}: '{text.strip()}'")
            
            try:
                # Method 1: Check parent and ancestor elements
                print("   🔍 Checking parent/ancestor elements:")
                current = element
                for level in range(5):  # Check up to 5 levels up
                    try:
                        parent = current.locator("xpath=..")
                        if parent.count() > 0:
                            parent_tag = parent.evaluate("element => element.tagName")
                            parent_class = parent.get_attribute("class") or ""
                            parent_id = parent.get_attribute("id") or ""
                            parent_text = (parent.text_content() or "")[:100].replace('\n', ' ').strip()
                            
                            print(f"     Level {level+1}: <{parent_tag}> class='{parent_class[:30]}' id='{parent_id}' text='{parent_text[:50]}'"[:120])
                            
                            # Look for court indicators
                            court_indicators = []
                            if "court" in parent_class.lower():
                                court_indicators.append(f"class contains 'court'")
                            if "court" in parent_text.lower():
                                court_indicators.append(f"text contains 'court'")
                            if any(str(i) in parent_class for i in range(1, 9)):
                                court_indicators.append(f"class contains number")
                            if parent_id:
                                court_indicators.append(f"has ID: {parent_id}")
                            
                            if court_indicators:
                                print(f"       🎯 COURT CLUES: {', '.join(court_indicators)}")
                            
                            current = parent
                        else:
                            break
                    except Exception as e:
                        print(f"     Level {level+1}: Error - {e}")
                        break
                
                # Method 2: Check sibling elements
                print("   🔍 Checking sibling elements:")
                try:
                    # Get parent and check its children
                    parent = element.locator("xpath=..")
                    if parent.count() > 0:
                        children = parent.locator("*")
                        children_count = children.count()
                        print(f"     Parent has {children_count} children")
                        
                        # Look for text in siblings that might indicate court
                        for j in range(min(10, children_count)):  # Check first 10 siblings
                            sibling = children.nth(j)
                            sibling_text = (sibling.text_content() or "").strip()
                            sibling_class = sibling.get_attribute("class") or ""
                            
                            if sibling_text and len(sibling_text) < 50:  # Short text likely to be labels
                                print(f"     Sibling {j}: '{sibling_text}' (class: {sibling_class[:20]})")
                                
                                # Check for court patterns
                                import re
                                court_pattern = r'(?:court|Court)\s*#?(\d+)'
                                match = re.search(court_pattern, sibling_text)
                                if match:
                                    print(f"       🎯 COURT FOUND: {match.group(0)}")
                
                except Exception as e:
                    print(f"     Sibling analysis error: {e}")
                
                # Method 3: Check nearby elements by selector
                print("   🔍 Checking nearby elements with court-related selectors:")
                court_selectors = [
                    "*:has-text('Court')",
                    "*:has-text('#')",
                    "[class*='court']",
                    "[id*='court']",
                    "th", "td",  # Table headers/cells might contain court info
                    ".col-header", ".row-header",  # Common header classes
                ]
                
                for selector in court_selectors:
                    try:
                        nearby = agent.page.locator(selector).filter(visible=True)
                        if nearby.count() > 0:
                            print(f"     Found {nearby.count()} elements matching '{selector}'")
                            
                            # Check first few
                            for k in range(min(3, nearby.count())):
                                nearby_element = nearby.nth(k)
                                nearby_text = (nearby_element.text_content() or "").strip()
                                if nearby_text and len(nearby_text) < 30:
                                    print(f"       '{nearby_text}'")
                    except:
                        pass
                
                print("   " + "-"*50)
                
            except Exception as e:
                print(f"   ❌ Error analyzing element {i+1}: {e}")
        
        print(f"\n🔍 Step 3: Look for schedule grid structure...")
        
        # Look for table structure or grid layout
        grid_selectors = [
            "table",
            "thead", "tbody",
            "tr", "th", "td",
            ".schedule-grid",
            ".calendar-grid",
            "[class*='grid']",
            "[class*='calendar']",
            "[class*='schedule']",
        ]
        
        for selector in grid_selectors:
            try:
                elements = agent.page.locator(selector).filter(visible=True)
                count = elements.count()
                if count > 0:
                    print(f"   {selector:20}: {count:4} elements")
                    
                    # Sample some content
                    if count <= 20:  # If not too many, sample them
                        for i in range(min(5, count)):
                            element = elements.nth(i)
                            text = (element.text_content() or "").strip()[:50]
                            classes = element.get_attribute("class") or ""
                            if text:
                                print(f"     Sample {i+1}: '{text}' (class: {classes[:30]})")
            except:
                pass
        
        print(f"\n🔍 Step 4: Manual inspection time...")
        print("Please examine the browser window and note:")
        print("  • How are the courts labeled/arranged?")
        print("  • Are there column headers showing court numbers?")
        print("  • Are there row headers showing times?")
        print("  • Is it a table or div-based grid?")
        print("  • What's the overall layout structure?")
        
        print("\n⏰ Browser staying open for 60 seconds for manual inspection...")
        time.sleep(60)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ Court detection analysis completed!")
    print("Next steps:")
    print("  1. Review the parent/sibling analysis above")
    print("  2. Look for patterns in the DOM structure")
    print("  3. Identify how to map bookings to courts")
    print("  4. Update the court detection logic accordingly")

if __name__ == "__main__":
    analyze_court_detection()
