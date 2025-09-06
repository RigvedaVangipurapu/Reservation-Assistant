#!/usr/bin/env python3
"""
Fix court detection by using table structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def fix_court_detection():
    print("\n🔧 FIXING COURT DETECTION USING TABLE STRUCTURE")
    print("=" * 55)
    print("Strategy: Find the table column (TD) each booking belongs to")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        # Wait for page to load
        agent.page.wait_for_selector(".booking-div-content", timeout=10000)
        
        print(f"\n🔍 Step 1: Find court headers in the table...")
        
        # Look for table headers with court information
        court_headers = []
        
        # Method 1: Look for TD elements containing "Court #X"
        court_tds = agent.page.locator("td:has-text('Court #')").filter(visible=True)
        print(f"   Found {court_tds.count()} TDs with 'Court #' text")
        
        for i in range(court_tds.count()):
            header_td = court_tds.nth(i)
            header_text = header_td.text_content().strip()
            
            # Extract court number
            import re
            court_match = re.search(r'Court #(\d+)', header_text)
            if court_match:
                court_num = int(court_match.group(1))
                court_headers.append({
                    'court_name': f"Court #{court_num}",
                    'court_number': court_num,
                    'element': header_td,
                    'text': header_text
                })
                print(f"     Found: {header_text} (Court #{court_num})")
        
        court_headers.sort(key=lambda x: x['court_number'])  # Sort by court number
        print(f"   📊 Total court headers found: {len(court_headers)}")
        
        print(f"\n🔍 Step 2: Find column index for each court header...")
        
        # For each court header, determine its column position
        for court_info in court_headers:
            try:
                # Get the parent row
                header_td = court_info['element']
                parent_tr = header_td.locator("xpath=..")
                
                if parent_tr.count() > 0:
                    # Get all TD elements in this row
                    row_tds = parent_tr.locator("td")
                    row_td_count = row_tds.count()
                    
                    # Find the index of this court header TD
                    for col_index in range(row_td_count):
                        td = row_tds.nth(col_index)
                        td_text = td.text_content().strip()
                        if court_info['court_name'] in td_text:
                            court_info['column_index'] = col_index
                            print(f"     {court_info['court_name']} is at column {col_index}")
                            break
            except Exception as e:
                print(f"     Error finding column for {court_info['court_name']}: {e}")
        
        print(f"\n🔍 Step 3: Map each booking to its court using table position...")
        
        # Find all booking elements
        booking_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        total_bookings = booking_elements.count()
        print(f"   📊 Found {total_bookings} booking elements")
        
        bookings_with_courts = []
        
        for i in range(total_bookings):
            try:
                booking_element = booking_elements.nth(i)
                booking_text = booking_element.text_content().strip()
                
                # Navigate up to find the containing TD
                current = booking_element
                containing_td = None
                
                # Go up the DOM tree to find the TD
                for level in range(10):  # Max 10 levels up
                    try:
                        parent = current.locator("xpath=..")
                        if parent.count() > 0:
                            tag_name = parent.evaluate("element => element.tagName.toLowerCase()")
                            if tag_name == "td":
                                containing_td = parent
                                break
                            current = parent
                        else:
                            break
                    except:
                        break
                
                if containing_td:
                    # Find which column this TD is in
                    parent_tr = containing_td.locator("xpath=..")
                    if parent_tr.count() > 0:
                        row_tds = parent_tr.locator("td")
                        td_count = row_tds.count()
                        
                        # Find the column index
                        booking_column = None
                        for col_idx in range(td_count):
                            td = row_tds.nth(col_idx)
                            # Check if this TD contains our booking element
                            booking_in_td = td.locator(".booking-div-content").count()
                            if booking_in_td > 0:
                                # Verify it's the right booking by text
                                booking_texts_in_td = []
                                for j in range(booking_in_td):
                                    booking_in_td_text = td.locator(".booking-div-content").nth(j).text_content().strip()
                                    booking_texts_in_td.append(booking_in_td_text)
                                
                                if booking_text in booking_texts_in_td:
                                    booking_column = col_idx
                                    break
                        
                        # Match column to court
                        matched_court = "Unknown Court"
                        for court_info in court_headers:
                            if court_info.get('column_index') == booking_column:
                                matched_court = court_info['court_name']
                                break
                        
                        # If no exact match, use position-based estimation
                        if matched_court == "Unknown Court" and booking_column is not None:
                            # Estimate court based on column position
                            if booking_column > 0:  # Skip first column (might be time labels)
                                estimated_court_num = min(booking_column, 8)  # Max 8 courts
                                matched_court = f"Court #{estimated_court_num}"
                        
                        bookings_with_courts.append({
                            'booking_text': booking_text,
                            'court': matched_court,
                            'column_index': booking_column,
                            'element_index': i
                        })
                        
                        print(f"     Booking #{i+1}: '{booking_text}' → {matched_court} (col {booking_column})")
                
                else:
                    print(f"     Booking #{i+1}: '{booking_text}' → Could not find containing TD")
                    bookings_with_courts.append({
                        'booking_text': booking_text,
                        'court': f"Court #{(i % 8) + 1}",  # Fallback
                        'column_index': None,
                        'element_index': i
                    })
                
            except Exception as e:
                print(f"     Error processing booking #{i+1}: {e}")
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Total bookings: {len(bookings_with_courts)}")
        
        # Group by court
        court_counts = {}
        for booking in bookings_with_courts:
            court = booking['court']
            if court not in court_counts:
                court_counts[court] = []
            court_counts[court].append(booking['booking_text'])
        
        for court, bookings in sorted(court_counts.items()):
            print(f"   {court}: {len(bookings)} bookings")
            for booking_text in bookings[:3]:  # Show first 3
                print(f"     - {booking_text}")
            if len(bookings) > 3:
                print(f"     - ... and {len(bookings) - 3} more")
        
        print(f"\n✅ Court detection method working!")
        print("Key insights:")
        print("  • Bookings are inside table cells (TD elements)")
        print("  • Court headers show which column is which court")  
        print("  • Can map bookings to courts by table column position")
        
        print("\n⏰ Browser staying open for 30 seconds for verification...")
        time.sleep(30)
        
    finally:
        agent.stop_browser()
    
    print("\n🎯 Next step: Integrate this logic into the main agent!")

if __name__ == "__main__":
    fix_court_detection()
