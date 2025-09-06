#!/usr/bin/env python3
"""
Badminton Court Booking Assistant - Streamlit GUI
================================================

A modern, user-friendly web interface for the Badminton Court Booking Agent.
This Streamlit application provides an intuitive chat-based interface that allows
users to book badminton courts using natural language requests.

Key Features:
- Chat-based interaction with message history
- Dark mode compatibility with custom CSS styling
- Real-time processing with loading indicators
- Responsive design for various screen sizes
- Visitor mode warnings and limitations display
- Quick suggestion buttons for common requests

Architecture:
- Session State: Manages user interactions and booking state
- Enhanced Booking Agent: Handles the core booking logic
- Message System: Displays chat history with proper formatting
- Form Handling: Manages user input and form submissions

User Experience:
- Natural language input for booking requests
- Visual feedback during processing
- Clear error messages and suggestions
- Booking confirmation workflow
- Alternative time slot suggestions

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

# ============================================================================
# IMPORTS AND CONFIGURATION
# ============================================================================

import streamlit as st
import os
from datetime import datetime, timedelta
from badminton_agent import BookingAgent
from booking_engine import EnhancedBookingAgent, BookingStatus
import time

# Configure page
st.set_page_config(
    page_title="🏸 Badminton Court Booking Assistant",
    page_icon="🏸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling (dark mode friendly)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        border-left: 4px solid #666;
        background-color: rgba(240, 240, 240, 0.1);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.3);
    }
    .user-message {
        background-color: rgba(33, 150, 243, 0.15);
        border-left-color: #2196f3;
        text-align: right;
        color: inherit;
    }
    .bot-message {
        background-color: rgba(158, 158, 158, 0.15);
        border-left-color: #9e9e9e;
        color: inherit;
    }
    .success-message {
        background-color: rgba(76, 175, 80, 0.15);
        border-left-color: #4caf50;
        color: inherit;
    }
    .error-message {
        background-color: rgba(244, 67, 54, 0.15);
        border-left-color: #f44336;
        color: inherit;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        background-color: #2196f3;
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        color: inherit;
    }
    /* Dark mode specific adjustments */
    @media (prefers-color-scheme: dark) {
        .chat-message {
            background-color: rgba(64, 64, 64, 0.3);
            color: #ffffff;
        }
        .user-message {
            background-color: rgba(33, 150, 243, 0.2);
            color: #ffffff;
        }
        .bot-message {
            background-color: rgba(96, 96, 96, 0.3);
            color: #ffffff;
        }
        .success-message {
            background-color: rgba(76, 175, 80, 0.2);
            color: #ffffff;
        }
        .error-message {
            background-color: rgba(244, 67, 54, 0.2);
            color: #ffffff;
        }
    }
    /* Force high contrast text for better readability */
    .chat-message * {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🏸 Hi! I'm your badminton court booking assistant. Just tell me when you'd like to play!\n\nExamples:\n- \"Book me a court tomorrow at 7 PM\"\n- \"I need Court #2 today at 9 AM\"\n- \"Find me any available court this afternoon\"",
                "type": "welcome"
            }
        ]
    
    if 'booking_agent' not in st.session_state:
        st.session_state.booking_agent = None
    
    if 'enhanced_agent' not in st.session_state:
        st.session_state.enhanced_agent = None
    
    if 'pending_booking' not in st.session_state:
        st.session_state.pending_booking = None
    
    if 'booking_in_progress' not in st.session_state:
        st.session_state.booking_in_progress = False

def get_agent():
    """Get or create the booking agent"""
    if st.session_state.booking_agent is None:
        # Create agent in headless mode for GUI
        st.session_state.booking_agent = BookingAgent(headless=True, slow_mo=500)
        st.session_state.enhanced_agent = EnhancedBookingAgent(
            st.session_state.booking_agent, 
            use_ai_engine=False  # Use rule-based for consistency
        )
    return st.session_state.enhanced_agent

def add_message(role: str, content: str, message_type: str = "normal"):
    """Add a message to the chat"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "type": message_type,
        "timestamp": datetime.now()
    })

def display_message(message):
    """Display a single message with better contrast"""
    role = message["role"]
    content = message["content"]
    msg_type = message.get("type", "normal")
    
    # Escape HTML content for safety and better rendering
    content = content.replace('<', '&lt;').replace('>', '&gt;')
    
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>👤 You:</strong><br>{content}</div>', unsafe_allow_html=True)
    else:
        icon = "🏸" if msg_type == "welcome" else "🤖"
        css_class = "chat-message bot-message"
        
        if msg_type == "success":
            css_class = "chat-message success-message"
            icon = "✅"
        elif msg_type == "error":
            css_class = "chat-message error-message"
            icon = "❌"
        
        label = "Assistant" if msg_type != "welcome" else "Welcome"
        st.markdown(f'<div class="{css_class}"><strong>{icon} {label}:</strong><br>{content}</div>', unsafe_allow_html=True)

def process_booking_request(user_input: str):
    """Process a booking request"""
    try:
        agent = get_agent()
        
        # Show processing message
        with st.spinner("🔍 Searching for available courts..."):
            result = agent.book_court(user_input)
        
        if result.status == BookingStatus.FOUND_EXACT:
            # Found exact match, ask for confirmation
            slot = result.booked_slot
            content = f"🎾 Perfect! I found exactly what you wanted:\n\n"
            content += f"**{slot.court}** on **{slot.date}** at **{slot.time_range}**\n\n"
            content += "Would you like me to book this slot?"
            
            add_message("assistant", content, "success")
            st.session_state.pending_booking = result
            
        elif result.status == BookingStatus.FOUND_ALTERNATIVES:
            # Found alternatives, show options
            slot = result.booked_slot
            alternatives = result.alternatives
            
            content = f"🎾 Found a great match!\n\n"
            content += f"**Recommended:** {slot.court} on {slot.date} at {slot.time_range}\n\n"
            
            if alternatives:
                content += "**Other options:**\n"
                for i, alt in enumerate(alternatives[:3], 1):
                    content += f"{i}. {alt.court} at {alt.time_range}\n"
                content += "\n"
            
            # Add visitor mode warning if applicable
            if hasattr(result, 'metadata') and result.metadata.get('visitor_mode'):
                content += "⚠️ **Note:** This data is from visitor mode and may not reflect actual availability. Please verify on the website before making plans.\n\n"
            
            content += "Would you like me to book the recommended slot?"
            
            add_message("assistant", content)
            st.session_state.pending_booking = result
            
        elif result.status == BookingStatus.BOOKING_SUCCESS:
            # Booking completed successfully
            slot = result.booked_slot
            content = f"🎉 Booking successful!\n\n"
            content += f"**Booked:** {slot.court} on {slot.date} at {slot.time_range}\n\n"
            content += "You're all set! See you on the court! 🏸"
            
            add_message("assistant", content, "success")
            st.session_state.pending_booking = None
            
        elif result.status == BookingStatus.BOOKING_FAILED:
            # Booking failed
            content = "❌ " + result.user_message
            if result.alternatives:
                content += "\n\nHere are some alternatives you might consider:\n"
                for i, alt in enumerate(result.alternatives[:3], 1):
                    content += f"{i}. {alt.court} at {alt.time_range}\n"
            
            add_message("assistant", content, "error")
            st.session_state.pending_booking = None
            
        else:
            # No slots found
            content = result.user_message or "Sorry, I couldn't find any available courts for your request. Try a different time or date?"
            add_message("assistant", content, "error")
            st.session_state.pending_booking = None
            
    except Exception as e:
        error_msg = f"Oops! Something went wrong: {str(e)}\n\nPlease try again or rephrase your request."
        add_message("assistant", error_msg, "error")
        st.session_state.pending_booking = None

def confirm_booking():
    """Confirm and execute the pending booking"""
    if st.session_state.pending_booking:
        try:
            agent = get_agent()
            slot = st.session_state.pending_booking.booked_slot
            
            with st.spinner("📅 Booking your court..."):
                # Simulate booking process
                time.sleep(2)  # Brief delay for user experience
                result = agent.confirm_booking(slot)
            
            if result.success:
                content = f"🎉 Booking confirmed!\n\n"
                content += f"**Booked:** {slot.court} on {slot.date} at {slot.time_range}\n\n"
                content += "You're all set! See you on the court! 🏸"
                add_message("assistant", content, "success")
            else:
                content = f"❌ Booking failed: {result.message}\n\nThe slot may have been taken by someone else. Please try again."
                add_message("assistant", content, "error")
                
        except Exception as e:
            content = f"❌ Booking error: {str(e)}\n\nPlease try again."
            add_message("assistant", content, "error")
        
        st.session_state.pending_booking = None

def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header"><h1>🏸 Badminton Court Booking Assistant</h1></div>', unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display all messages
        for message in st.session_state.messages:
            display_message(message)
    
    # Input section
    st.markdown("---")
    
    # Check if we have a pending booking
    if st.session_state.pending_booking:
        st.markdown("### 🤔 Confirm Booking")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, Book It!", key="confirm_yes"):
                confirm_booking()
                st.experimental_rerun()
        
        with col2:
            if st.button("❌ No, Search Again", key="confirm_no"):
                st.session_state.pending_booking = None
                add_message("assistant", "No problem! Feel free to make another request. What would you like to book?")
                st.experimental_rerun()
    
    else:
        # Regular input
        with st.form("booking_form", clear_on_submit=True):
            st.markdown("### 💬 What would you like to book?")
            
            user_input = st.text_input(
                "Type your request...",
                value="",
                placeholder="e.g., Book me a court tomorrow at 7 PM"
            )
            
            # Main submit button
            submitted = st.form_submit_button("🏸 Submit Request")
            
            # Quick suggestions
            st.markdown("**Quick suggestions:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                morning_clicked = st.form_submit_button("🌅 Tomorrow morning")
            with col2:
                evening_clicked = st.form_submit_button("🌆 Tomorrow evening")
            with col3:
                check_clicked = st.form_submit_button("📅 Check availability")
            
        # Handle form submission
        if submitted and user_input:
            # Add user message
            add_message("user", user_input)
            
            # Process the request
            process_booking_request(user_input)
            
            # Rerun to show new messages
            st.experimental_rerun()
        
        # Handle quick suggestion buttons
        if morning_clicked:
            quick_request = "Book me a court tomorrow morning around 9 AM"
            add_message("user", quick_request)
            process_booking_request(quick_request)
            st.experimental_rerun()
        
        if evening_clicked:
            quick_request = "Book me a court tomorrow evening around 7 PM"
            add_message("user", quick_request)
            process_booking_request(quick_request)
            st.experimental_rerun()
        
        if check_clicked:
            quick_request = "What courts are available tomorrow?"
            add_message("user", quick_request)
            process_booking_request(quick_request)
            st.experimental_rerun()
    
    # Sidebar with info
    with st.sidebar:
        st.markdown("## ℹ️ How to Use")
        st.markdown("""
        **Just tell me what you want!**
        
        Examples:
        - "Book me a court tomorrow at 7 PM"
        - "I need Court #2 today at 9 AM"  
        - "Find me any court this afternoon"
        - "What's available tomorrow morning?"
        
        **Tips:**
        - Be specific about date and time
        - I'll show you options if exact match isn't available
        - You can request specific courts by number
        """)
        
        st.markdown("---")
        st.markdown("## ⚠️ Important Notice")
        st.markdown("""
        **Visitor Mode Limitations:**
        - This app runs in visitor mode
        - Data shown may not reflect actual availability
        - Use for planning purposes only
        - Always verify on the website before making plans
        - [Check OC Badminton Website](https://ocbadminton.skedda.com/booking)
        """)
        
        st.markdown("---")
        st.markdown("## 🔧 Settings")
        
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
            st.session_state.pending_booking = None
            st.experimental_rerun()
        
        if st.button("🛑 Reset Everything"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()
