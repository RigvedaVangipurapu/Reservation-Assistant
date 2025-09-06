#!/usr/bin/env python3
"""
Extract and display the raw HTML source code of all .booking-div-content elements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from badminton_agent import BookingAgent
import time

def extract_booking_html():
    print("\n📋 EXTRACTING RAW HTML FROM .booking-div-content ELEMENTS")
    print("=" * 65)
    print("This will show the exact HTML source code that the agent sees")
    
    agent = BookingAgent(headless=False, slow_mo=1000)
    
    try:
        print("\n🌐 Opening booking page...")
        agent.navigate_to_booking()
        
        target_date = "2025-09-10"
        print(f"\n📅 Navigating to {target_date}...")
        agent.change_date(target_date=target_date)
        
        print(f"\n🔍 Scanning for .booking-div-content elements...")
        
        # Wait for page to load
        try:
            agent.page.wait_for_selector(".booking-div-content", timeout=10000)
            print("✅ Found booking content elements")
        except:
            print("⚠️ No booking content found")
            return
        
        # Find all booking elements
        booking_elements = agent.page.locator(".booking-div-content").filter(visible=True)
        total_count = booking_elements.count()
        print(f"   📊 Total .booking-div-content elements found: {total_count}")
        
        if total_count == 0:
            print("❌ No booking elements found!")
            return
        
        print(f"\n📋 EXTRACTING HTML SOURCE FOR ALL {total_count} ELEMENTS:")
        print("=" * 65)
        
        for i in range(total_count):
            try:
                element = booking_elements.nth(i)
                
                # Extract different types of content
                inner_html = element.inner_html()
                outer_html = element.evaluate("element => element.outerHTML")
                text_content = element.text_content() or ""
                classes = element.get_attribute("class") or ""
                
                # Get parent element info
                parent_html = ""
                parent_classes = ""
                try:
                    parent = element.locator("xpath=..")
                    if parent.count() > 0:
                        parent_html = parent.evaluate("element => element.outerHTML")[:200] + "..."
                        parent_classes = parent.get_attribute("class") or ""
                except:
                    pass
                
                print(f"\n🔴 BOOKING ELEMENT #{i+1}:")
                print(f"   Classes: {classes}")
                print(f"   Text Content: '{text_content.strip()}'")
                print(f"   Inner HTML:")
                print(f"   {'-'*50}")
                print(f"   {inner_html}")
                print(f"   {'-'*50}")
                print(f"   Outer HTML:")
                print(f"   {'-'*50}")
                print(f"   {outer_html}")
                print(f"   {'-'*50}")
                
                if parent_html:
                    print(f"   Parent Element (first 200 chars):")
                    print(f"   Parent Classes: {parent_classes}")
                    print(f"   {parent_html}")
                
                print("\n" + "="*65)
                
                # Pause for readability if many elements
                if i > 0 and (i + 1) % 5 == 0:
                    print(f"\n⏸️  Showing element {i+1} of {total_count}. Continue? (showing next 5)")
                    time.sleep(2)
            
            except Exception as e:
                print(f"   ❌ Error processing element {i+1}: {e}")
                continue
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total elements processed: {total_count}")
        print(f"   Date: September 10th, 2025")
        print(f"   Page URL: {agent.page.url}")
        
        # Save all HTML to a file for detailed analysis
        print(f"\n💾 Saving detailed HTML analysis to file...")
        
        with open("booking_elements_analysis.html", "w", encoding="utf-8") as f:
            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n")
            f.write(f"<title>Booking Elements Analysis - {target_date}</title>\n")
            f.write(f"<style>body{{font-family: monospace; margin: 20px;}} .element{{border: 1px solid #ccc; margin: 10px 0; padding: 10px; background: #f9f9f9;}} .html{{background: #fff; border: 1px solid #ddd; padding: 10px; white-space: pre-wrap;}}</style>\n")
            f.write(f"</head>\n<body>\n")
            f.write(f"<h1>Booking Elements Analysis</h1>\n")
            f.write(f"<p>Date: {target_date} | Total Elements: {total_count} | URL: {agent.page.url}</p>\n")
            
            for i in range(total_count):
                element = booking_elements.nth(i)
                inner_html = element.inner_html()
                outer_html = element.evaluate("element => element.outerHTML")
                text_content = element.text_content() or ""
                classes = element.get_attribute("class") or ""
                
                f.write(f"<div class='element'>\n")
                f.write(f"<h3>Element #{i+1}</h3>\n")
                f.write(f"<p><strong>Classes:</strong> {classes}</p>\n")
                f.write(f"<p><strong>Text:</strong> '{text_content.strip()}'</p>\n")
                f.write(f"<h4>Inner HTML:</h4>\n")
                f.write(f"<div class='html'>{inner_html}</div>\n")
                f.write(f"<h4>Outer HTML:</h4>\n")
                f.write(f"<div class='html'>{outer_html}</div>\n")
                f.write(f"</div>\n")
            
            f.write(f"</body>\n</html>\n")
        
        print(f"   ✅ Saved to: booking_elements_analysis.html")
        
        print("\n⏰ Browser will stay open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    finally:
        agent.stop_browser()
    
    print("\n✅ HTML extraction completed!")
    print("You can now:")
    print("  1. Review the console output above")
    print("  2. Open 'booking_elements_analysis.html' in a browser")
    print("  3. Analyze the exact HTML structure the agent sees")

if __name__ == "__main__":
    extract_booking_html()
