#!/usr/bin/env python3
"""
Test script to explore the Skedda booking site and check authentication requirements
"""

from playwright.sync_api import sync_playwright
import time

def test_skedda_access():
    """Test if we can access the Skedda booking page without authentication"""
    
    with sync_playwright() as p:
        # Launch browser in visible mode for now
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # Add slow_mo for better debugging
        page = browser.new_page()
        
        # Set longer timeout
        page.set_default_timeout(60000)  # 60 seconds
        
        try:
            print("🌐 Navigating to OC Badminton Skedda page...")
            
            # Try going to main skedda page first
            page.goto("https://ocbadminton.skedda.com/")
            print("✅ Successfully loaded main page")
            
            # Wait for page to load
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)
            
            # Check what we can see
            title = page.title()
            print(f"📄 Page title: {title}")
            
            # Check if we're redirected to login
            current_url = page.url
            print(f"🔗 Current URL: {current_url}")
            
            # Try to navigate to booking page now
            print("🎯 Trying to navigate to booking page...")
            page.goto("https://ocbadminton.skedda.com/booking")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            
            current_url = page.url
            print(f"🔗 Booking page URL: {current_url}")
            
            # Look for common elements
            if "login" in current_url.lower() or "sign" in current_url.lower():
                print("🔐 Authentication required - redirected to login page")
                
                # Look for login form elements
                login_elements = page.locator("input[type='email'], input[type='text'], input[name*='email'], input[name*='username']")
                password_elements = page.locator("input[type='password']")
                
                print(f"📧 Email/username fields found: {login_elements.count()}")
                print(f"🔑 Password fields found: {password_elements.count()}")
                
                # Look for any login buttons or text
                page_text = page.inner_text("body")
                if "login" in page_text.lower() or "sign in" in page_text.lower():
                    print("🔍 Login-related text found on page")
                
            else:
                print("✅ No authentication redirect - checking what's available...")
                
                # Look for booking interface elements
                calendar_elements = page.locator("[class*='calendar'], [class*='booking'], [class*='schedule']")
                date_elements = page.locator("input[type='date'], [class*='date']")
                
                print(f"📅 Calendar/booking elements found: {calendar_elements.count()}")
                print(f"📆 Date input elements found: {date_elements.count()}")
                
                # Get page content to understand structure
                page_text = page.inner_text("body")
                print(f"📄 Page content preview: {page_text[:200]}...")
                
            # Take a screenshot for reference
            page.screenshot(path="/Users/rigvedavangipurapu/Documents/Reservation Assistant/skedda_page.png")
            print("📸 Screenshot saved as 'skedda_page.png'")
            
            # Keep browser open for a moment to inspect
            print("🔍 Browser will stay open for 15 seconds for manual inspection...")
            print("👀 Please check the browser window to see what's displayed")
            time.sleep(15)
            
        except Exception as e:
            print(f"❌ Error accessing Skedda: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_skedda_access()
