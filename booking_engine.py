#!/usr/bin/env python3
"""
Advanced Booking Engine - Robust, extensible booking logic
=========================================================

This module provides the intelligent booking logic that powers the Badminton Court
Booking Agent. It implements a sophisticated workflow system that can handle
complex booking requests, natural language processing, and intelligent decision-making.

Key Components:
- RequestParser: Converts natural language to structured booking requests
- BookingWorkflow: Orchestrates the complete booking process
- DecisionEngine: Makes intelligent decisions about booking actions
- EnhancedBookingAgent: High-level interface for booking operations

Architecture:
The system is designed with extensibility in mind, supporting both rule-based
and AI-powered decision-making. The modular design allows for easy integration
of new features and booking strategies.

Key Features:
- Natural language processing for dates, times, and court preferences
- Intelligent slot matching with preference scoring
- Alternative suggestion system
- Visitor mode handling with appropriate warnings
- Extensible decision engine architecture

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

# ============================================================================
# IMPORTS AND CONFIGURATION
# ============================================================================

import os
import json
import time
from typing import Dict, List, Optional, Any, Callable, Union, Protocol
from datetime import datetime, timedelta, time as time_obj
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import re

@dataclass
class TimeSlot:
    """Enhanced time slot representation"""
    court: str
    start_time: str
    end_time: str
    date: str
    available: bool
    price: Optional[float] = None
    duration_minutes: Optional[int] = None
    element_selector: Optional[str] = None
    booking_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def time_range(self) -> str:
        return f"{self.start_time}–{self.end_time}"
    
    @property
    def datetime_start(self) -> datetime:
        """Convert to datetime object for easier comparison"""
        date_str = f"{self.date} {self.start_time}"
        return datetime.strptime(date_str, "%Y-%m-%d %I:%M %p")
    
    def contains_time(self, target_time: str) -> bool:
        """Check if this slot contains a specific time"""
        try:
            target = datetime.strptime(f"{self.date} {target_time}", "%Y-%m-%d %I:%M %p")
            start = self.datetime_start
            end_str = f"{self.date} {self.end_time}"
            end = datetime.strptime(end_str, "%Y-%m-%d %I:%M %p")
            return start <= target <= end
        except:
            return False

class BookingStrategy(Enum):
    """Different booking strategies"""
    EXACT_MATCH = "exact_match"           # Only book exact request
    SMART_FALLBACK = "smart_fallback"     # Try exact, then suggest alternatives
    FLEXIBLE = "flexible"                 # Accept close matches automatically
    INTERACTIVE = "interactive"           # Always ask user for confirmation

class InteractionMode(Enum):
    """Different interaction modes"""
    AUTOMATED = "automated"               # Fully automated booking
    CONFIRMATION = "confirmation"         # Show options, get confirmation
    HYBRID = "hybrid"                    # Mix of automated + confirmation as needed

class BookingStatus(Enum):
    """Booking process status"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    FOUND_EXACT = "found_exact"
    FOUND_ALTERNATIVES = "found_alternatives"
    USER_CONFIRMATION_NEEDED = "user_confirmation_needed"
    BOOKING_IN_PROGRESS = "booking_in_progress"
    BOOKING_SUCCESS = "booking_success"
    BOOKING_FAILED = "booking_failed"
    CANCELLED = "cancelled"

@dataclass
class BookingRequest:
    """User's booking request with parsed details"""
    raw_request: str
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    preferred_court: Optional[str] = None
    duration_minutes: Optional[int] = None
    flexibility_minutes: int = 30  # How flexible on time
    max_alternatives: int = 3
    strategy: BookingStrategy = BookingStrategy.SMART_FALLBACK
    interaction_mode: InteractionMode = InteractionMode.CONFIRMATION
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BookingResult:
    """Result of a booking operation"""
    status: BookingStatus
    success: bool
    message: str
    booked_slot: Optional[TimeSlot] = None
    alternatives: List[TimeSlot] = field(default_factory=list)
    user_message: str = ""
    next_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class RequestParser:
    """Parse natural language booking requests"""
    
    def __init__(self):
        self.time_patterns = [
            r'(\d{1,2}):?(\d{2})?\s*(am|pm)',
            r'(\d{1,2})\s*o\'?clock',
            r'(\d{1,2}):(\d{2})',
        ]
        
        self.date_patterns = [
            r'tomorrow',
            r'today', 
            r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'(\d{1,2})/(\d{1,2})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'(\d{4})-(\d{2})-(\d{2})',
            # Patterns with year
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+(\d{4})',
            r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*(\d{4})',
            # Patterns without year (default to 2025)
            r'(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)',
            r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+(\d{1,2})(?:st|nd|rd|th)?',
        ]
        
        self.court_patterns = [
            r'court\s*#?(\d+)',
            r'court\s+([a-zA-Z]\w*)',  # More specific - starts with letter
        ]
    
    def parse(self, request: str) -> BookingRequest:
        """Parse natural language request into structured data - let AI handle everything"""
        request_lower = request.lower()
        
        # Let AI handle ALL parsing - no regex patterns
        # Just pass the raw request to AI for complete understanding
        
        # Determine strategy from keywords
        strategy = BookingStrategy.SMART_FALLBACK
        if any(word in request_lower for word in ['exact', 'exactly', 'specifically']):
            strategy = BookingStrategy.EXACT_MATCH
        elif any(word in request_lower for word in ['flexible', 'around', 'approximately']):
            strategy = BookingStrategy.FLEXIBLE
        
        # Determine interaction mode
        interaction_mode = InteractionMode.CONFIRMATION
        if any(word in request_lower for word in ['just book', 'automatically', 'book immediately']):
            interaction_mode = InteractionMode.AUTOMATED
        
        # Extract date from request using AI
        # The raw request will be passed to the agent's AI-powered date parser
        # We'll let the agent handle the actual date parsing
        
        # Extract time and court preferences
        # Look for time patterns like "5pm", "after 5pm", "from 5pm"
        time_match = re.search(r'(?:after|from|at)?\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))', request_lower)
        preferred_time = time_match.group(1) if time_match else None
        
        # Check if it's "after" or "from" a time
        is_after_time = bool(re.search(r'(?:after|from)\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)', request_lower))
        
        # Create metadata
        metadata = {}
        if is_after_time and preferred_time:
            metadata["after_time"] = preferred_time
        
        court_match = re.search(r'court\s*#?\s*(\d+)', request_lower)
        preferred_court = f"Court #{court_match.group(1)}" if court_match else None
        
        return BookingRequest(
            raw_request=request,  # Pass the full request for AI parsing
            preferred_date=None,  # Let agent's AI handle date parsing
            preferred_time=preferred_time,  # Basic time extraction
            preferred_court=preferred_court,  # Basic court extraction
            strategy=strategy,
            interaction_mode=interaction_mode,
            metadata=metadata  # Pass metadata with after_time if present
        )
    
    def _extract_time(self, text: str) -> Optional[str]:
        """Extract time from text"""
        for pattern in self.time_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) >= 3:  # Full time with AM/PM
                    hour, minute, ampm = match.groups()
                    minute = minute or "00"
                    return f"{hour}:{minute} {ampm.upper()}"
                elif len(match.groups()) == 1:  # Just hour
                    hour = match.groups()[0]
                    # Guess AM/PM based on context
                    ampm = "PM" if int(hour) <= 11 and int(hour) >= 6 else "AM"
                    return f"{hour}:00 {ampm}"
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract date from text"""
        if 'tomorrow' in text:
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif 'today' in text:
            return datetime.now().strftime("%Y-%m-%d")
        
        # Month name to number mapping (including abbreviations)
        months = {
            'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 
            'march': 3, 'mar': 3, 'april': 4, 'apr': 4,
            'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7, 
            'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 
            'december': 12, 'dec': 12
        }
        
        # Try other patterns
        for pattern in self.date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                try:
                    if 'next' in pattern:
                        # Handle "next Monday" etc.
                        weekday = groups[0]
                        # Implementation for next weekday calculation
                        pass
                    
                    elif len(groups) == 3 and any(month in pattern for month in months.keys()):
                        # Handle "9th September 2025" or "September 9th, 2025"
                        if pattern.startswith(r'(\d{1,2})'):
                            # "9th September 2025" format
                            day, month_name, year = groups
                        else:
                            # "September 9th, 2025" format  
                            month_name, day, year = groups
                        
                        month_num = months.get(month_name.lower())
                        if month_num:
                            # Remove ordinal suffixes (st, nd, rd, th)
                            day = re.sub(r'(st|nd|rd|th)', '', day)
                            # If no year provided, default to 2025
                            if not year:
                                year = "2025"
                            return f"{year}-{month_num:02d}-{int(day):02d}"
                    
                    elif len(groups) == 2 and any(month in pattern for month in months.keys()):
                        # Handle "9th September" or "September 9th" (no year - default to 2025)
                        if pattern.startswith(r'(\d{1,2})'):
                            # "9th September" format
                            day, month_name = groups
                        else:
                            # "September 9th" format  
                            month_name, day = groups
                        
                        month_num = months.get(month_name.lower())
                        if month_num:
                            # Remove ordinal suffixes (st, nd, rd, th)
                            day = re.sub(r'(st|nd|rd|th)', '', day)
                            # Default to 2025 when no year provided
                            return f"2025-{month_num:02d}-{int(day):02d}"
                    
                    elif len(groups) == 3 and groups[2]:  # MM/DD/YYYY
                        month, day, year = groups
                        return f"{year}-{int(month):02d}-{int(day):02d}"
                    
                    elif len(groups) == 2:  # MM/DD (default to 2025)
                        month, day = groups
                        return f"2025-{int(month):02d}-{int(day):02d}"
                    
                    elif len(groups) == 3 and '-' in text:  # YYYY-MM-DD
                        year, month, day = groups
                        return f"{year}-{month}-{day}"
                        
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def _extract_court(self, text: str) -> Optional[str]:
        """Extract court preference from text"""
        for pattern in self.court_patterns:
            match = re.search(pattern, text)
            if match:
                court_id = match.groups()[0]
                # Only return if court_id is actually a number or valid court name
                # Exclude common false positives
                excluded_words = ['tomorrow', 'today', 'this', 'that', 'the', 'any', 'some', 'on', 'at', 'for', 'me', 'a', 'an']
                if court_id.lower() not in excluded_words and (court_id.isdigit() or court_id.isalpha()):
                    return f"Court #{court_id}"
        return None

class DecisionEngine(ABC):
    """Abstract base for decision engines (rule-based, AI-powered, hybrid)"""
    
    @abstractmethod
    def find_best_slots(self, 
                       request: BookingRequest, 
                       available_slots: List[TimeSlot]) -> List[TimeSlot]:
        """Find the best matching slots for a request"""
        pass
    
    @abstractmethod
    def should_auto_book(self, 
                        request: BookingRequest, 
                        best_slot: TimeSlot) -> bool:
        """Decide if we should auto-book or ask for confirmation"""
        pass

class RuleBasedDecisionEngine(DecisionEngine):
    """Rule-based decision engine for deterministic booking logic"""
    
    def find_best_slots(self, 
                       request: BookingRequest, 
                       available_slots: List[TimeSlot]) -> List[TimeSlot]:
        """Use AI to find best matching slots based on user's request"""
        
        if not available_slots:
            return []
        
        # Format slots for AI
        slots_text = []
        for slot in available_slots:
            slots_text.append(f"- {slot.court} at {slot.time_range} on {slot.date}")
        
        # Create prompt for AI
        prompt = f"""
        User Request: "{request.raw_request}"
        
        Available Slots:
        {chr(10).join(slots_text)}
        
        Based on the user's request, select the most suitable slots. Consider:
        1. Date preferences (explicit or implied)
        2. Time preferences (specific times, "after X", "evening", etc.)
        3. Court preferences (if mentioned)
        4. Duration preferences (if mentioned)
        
        Return ONLY the exact slot text for the best matches (max 5 slots), one per line.
        Example return format:
        Court #1 at 7:00 PM–8:00 PM on 2025-09-10
        Court #2 at 7:00 PM–8:00 PM on 2025-09-10
        
        Selected slots:
        """
        
        try:
            # Get AI's selection
            response = self.model.generate_content(prompt)
            selected_texts = response.text.strip().split('\n')
            
            # Match selected texts back to TimeSlot objects
            selected_slots = []
            for text in selected_texts:
                text = text.strip()
                if not text:
                    continue
                    
                # Find matching slot
                for slot in available_slots:
                    slot_text = f"{slot.court} at {slot.time_range} on {slot.date}"
                    if text in slot_text or slot_text in text:
                        selected_slots.append(slot)
                        break
            
            print(f"🤖 AI selected {len(selected_slots)} slots based on request")
            return selected_slots[:request.max_alternatives]
            
        except Exception as e:
            print(f"⚠️ AI slot selection failed: {e}")
            # Fallback to first few slots
            return available_slots[:request.max_alternatives]
    
    def _calculate_time_score(self, slot: TimeSlot, preferred_time: str, flexibility_minutes: int) -> float:
        """Calculate how well a slot matches the preferred time"""
        try:
            # Check if preferred time falls within the slot duration first
            if slot.contains_time(preferred_time):
                return 1.0  # Perfect match - time is within the slot
            
            # Parse preferred time for proximity scoring
            pref_dt = datetime.strptime(f"{slot.date} {preferred_time}", "%Y-%m-%d %I:%M %p")
            slot_start = slot.datetime_start
            
            # Calculate time difference in minutes
            diff_minutes = abs((slot_start - pref_dt).total_seconds() / 60)
            
            # If within flexibility range, calculate score (closer = higher score)
            if diff_minutes <= flexibility_minutes:
                # Score from 0.8 (exact start time match) to 0.1 (at flexibility limit)
                score = 0.8 - (diff_minutes / flexibility_minutes) * 0.7
                return score
            
            return 0.0  # Outside flexibility range
            
        except Exception as e:
            # Try simpler time comparison if datetime parsing fails
            try:
                # Extract just the time part for comparison
                if preferred_time.replace(' ', '').lower() in slot.time_range.replace(' ', '').lower():
                    return 0.5  # Partial match
                return 0.0
            except:
                return 0.0
    
    def should_auto_book(self, request: BookingRequest, best_slot: TimeSlot) -> bool:
        """Rule-based decision for auto-booking"""
        
        if request.interaction_mode == InteractionMode.AUTOMATED:
            return True
        
        if request.strategy == BookingStrategy.EXACT_MATCH:
            # Only auto-book if it's an exact match
            if request.preferred_time and best_slot.contains_time(request.preferred_time):
                return request.interaction_mode != InteractionMode.CONFIRMATION
        
        return False

class AIDecisionEngine(DecisionEngine):
    """AI-powered decision engine for intelligent booking decisions"""
    
    def __init__(self, model):
        self.model = model
    
    def find_best_slots(self, 
                       request: BookingRequest, 
                       available_slots: List[TimeSlot]) -> List[TimeSlot]:
        """Use AI to find best matching slots based on user's request"""
        
        if not available_slots:
            return []
        
        # Format slots for AI
        slots_text = []
        for slot in available_slots:
            slots_text.append(f"- {slot.court} at {slot.time_range} on {slot.date}")
        
        # Create prompt for AI
        prompt = f"""
        You are a badminton court booking assistant. Find the best matching slots for this request.
        
        User Request: "{request.raw_request}"
        
        Available Slots:
        {chr(10).join(slots_text)}
        
        CRITICAL REQUIREMENTS:
        1. Return ONLY the exact slot text for the best matches (max 5 slots), one per line
        2. Match the exact format: "Court #X at H:MM AM/PM–H:MM AM/PM on YYYY-MM-DD"
        3. STRICTLY follow time preferences:
           - If user says "after X", ONLY show slots that start after that time
           - If user says "evening", show slots after 5 PM
           - If user says "morning", show slots before 12 PM
           - If user says "afternoon", show slots between 12 PM and 5 PM
        4. Sort slots by best match first (closest to requested time)
        5. Return NOTHING ELSE - no explanations or extra text
        
        Example return format:
        Court #1 at 7:00 PM–8:00 PM on 2025-09-10
        Court #2 at 7:00 PM–8:00 PM on 2025-09-10
        
        Selected slots:
        """
        
        try:
            # Get AI's selection
            response = self.model.generate_content(prompt)
            selected_texts = response.text.strip().split('\n')
            
            # Match selected texts back to TimeSlot objects
            selected_slots = []
            for text in selected_texts:
                text = text.strip()
                if not text:
                    continue
                    
                # Find matching slot
                for slot in available_slots:
                    slot_text = f"{slot.court} at {slot.time_range} on {slot.date}"
                    if text in slot_text or slot_text in text:
                        selected_slots.append(slot)
                        break
            
            print(f"🤖 AI selected {len(selected_slots)} slots based on request")
            return selected_slots[:request.max_alternatives]
            
        except Exception as e:
            print(f"⚠️ AI slot selection failed: {e}")
            # Fallback to first few slots
            return available_slots[:request.max_alternatives]
    
    def should_auto_book(self, request: BookingRequest, best_slot: TimeSlot) -> bool:
        """Use AI to decide on auto-booking"""
        
        # Use AI to make nuanced decisions
        context = f"""
        User Request: {request.raw_request}
        Best Slot Found: {best_slot.court} on {best_slot.date} at {best_slot.time_range}
        Strategy: {request.strategy.value}
        Interaction Mode: {request.interaction_mode.value}
        
        Should this be automatically booked (true) or should we ask for user confirmation (false)?
        Consider the user's intent and the quality of the match.
        
        Respond with just 'true' or 'false'.
        """
        
        try:
            response = self.model.generate_content(context)
            return 'true' in response.text.lower()
        except:
            # Fallback to rule-based
            rule_engine = RuleBasedDecisionEngine()
            return rule_engine.should_auto_book(request, best_slot)

class BookingWorkflow:
    """Manages the booking workflow and state transitions"""
    
    def __init__(self, agent, decision_engine: DecisionEngine):
        self.agent = agent
        self.decision_engine = decision_engine
        self.current_request: Optional[BookingRequest] = None
        self.current_status = BookingStatus.PENDING
        self.workflow_history: List[Dict[str, Any]] = []
    
    def execute_booking(self, request: BookingRequest) -> BookingResult:
        """Execute the complete booking workflow"""
        
        self.current_request = request
        self.current_status = BookingStatus.ANALYZING
        
        try:
            # Step 1: Get available slots
            available_slots = self._get_available_slots(request)
            
            if not available_slots:
                return BookingResult(
                    status=BookingStatus.BOOKING_FAILED,
                    success=False,
                    message="No available slots found for the requested date/time",
                    user_message="Sorry, no courts are available for your requested time. Please try a different date or time."
                )
            
            # Step 2: Find best matches using decision engine
            best_slots = self.decision_engine.find_best_slots(request, available_slots)
            
            if not best_slots:
                return BookingResult(
                    status=BookingStatus.BOOKING_FAILED,
                    success=False,
                    message="No suitable slots found within preferences",
                    user_message="No courts match your specific requirements. Try being more flexible with your time preferences."
                )
            
            best_slot = best_slots[0]
            alternatives = best_slots[1:] if len(best_slots) > 1 else []
            
            # Step 3: Decide on booking strategy
            if self.decision_engine.should_auto_book(request, best_slot):
                # Auto-book the best slot
                return self._attempt_booking(best_slot, alternatives)
            else:
                # Request user confirmation
                self.current_status = BookingStatus.USER_CONFIRMATION_NEEDED
                
                # Add visitor mode warning to the message
                user_message = self._generate_confirmation_message(best_slot, alternatives)
                if hasattr(self, 'visitor_mode_info') and self.visitor_mode_info.get("visitor_mode"):
                    user_message += "\n\n⚠️ **Important:** This data is from visitor mode and may not reflect actual availability. Please verify on the website before making plans."
                
                return BookingResult(
                    status=BookingStatus.FOUND_EXACT if not alternatives else BookingStatus.FOUND_ALTERNATIVES,
                    success=False,  # Not booked yet
                    message="Found suitable slots, waiting for user confirmation",
                    booked_slot=best_slot,
                    alternatives=alternatives,
                    user_message=user_message,
                    next_action="confirm_booking",
                    metadata=getattr(self, 'visitor_mode_info', {})
                )
                
        except Exception as e:
            return BookingResult(
                status=BookingStatus.BOOKING_FAILED,
                success=False,
                message=f"Booking workflow error: {e}",
                user_message="Sorry, there was an error processing your booking request. Please try again."
            )
    
    def confirm_booking(self, slot: TimeSlot) -> BookingResult:
        """Confirm and execute a specific booking"""
        return self._attempt_booking(slot, [])
    
    def _get_available_slots(self, request: BookingRequest) -> List[TimeSlot]:
        """Get available slots from the agent"""
        
        # Navigate if needed
        if not self.agent.page:
            nav_result = self.agent.navigate_to_booking()
            if not nav_result["success"]:
                return []
        
        # Extract date using AI
        # First, try to extract just the date part from the request
        date_text = ""
        request_lower = request.raw_request.lower()
        
        # Look for date-related parts in the request
        date_indicators = [
            "today", "tomorrow", "next", "on", "for",
            "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ]
        
        words = request_lower.split()
        for i, word in enumerate(words):
            if any(indicator in word for indicator in date_indicators):
                # Take this word and the next few words as the date part
                date_text = " ".join(words[i:i+4])
                break
            elif word.replace("th", "").replace("st", "").replace("nd", "").replace("rd", "").isdigit():
                # Take this word and the next few words as the date part
                date_text = " ".join(words[i:i+3])
                break
        
        # If no date part found, use the whole request
        if not date_text:
            date_text = request.raw_request
        
        # Let AI parse the date
        print(f"🔍 Extracting date from: '{date_text}'")
        date_result = self.agent.change_date(date=date_text)
        
        # Get slots
        slots_result = self.agent.get_available_slots()
        if slots_result.get("error"):
            return []
        
        # Store visitor mode info for later use
        self.visitor_mode_info = {
            "visitor_mode": slots_result.get("visitor_mode", False),
            "limitations": slots_result.get("limitations", []),
            "recommendation": slots_result.get("recommendation")
        }
        
        # Convert to TimeSlot objects
        time_slots = []
        for slot_data in slots_result.get("slots", []):
            if slot_data.get("available", False):
                # Parse time range
                time_range = slot_data.get("time", "")
                if "–" in time_range:
                    start_time, end_time = time_range.split("–")
                else:
                    start_time = time_range
                    end_time = time_range
                
                # Get the correct date from the agent's current state
                current_date = self.agent.current_state.get("current_date", datetime.now().strftime("%Y-%m-%d"))
                
                time_slot = TimeSlot(
                    court=slot_data.get("court", "Unknown Court"),
                    start_time=start_time.strip(),
                    end_time=end_time.strip(),
                    date=current_date,
                    available=True
                )
                time_slots.append(time_slot)
        
        visitor_warning = " (VISITOR MODE)" if self.visitor_mode_info.get("visitor_mode") else ""
        print(f"🔍 Found {len(time_slots)} time slots from website{visitor_warning}:")
        for i, slot in enumerate(time_slots[:5]):  # Show first 5
            print(f"   {i+1}. {slot.court} - {slot.time_range} on {slot.date}")
        
        if self.visitor_mode_info.get("visitor_mode"):
            print("⚠️  WARNING: Running in visitor mode - data may not be accurate")
        
        return time_slots
    
    def _attempt_booking(self, slot: TimeSlot, alternatives: List[TimeSlot]) -> BookingResult:
        """Attempt to book a specific slot"""
        
        self.current_status = BookingStatus.BOOKING_IN_PROGRESS
        
        try:
            # Attempt the actual booking
            click_result = self.agent.click_time_slot(slot.court, slot.time_range)
            
            if click_result["success"]:
                # Check if booking was successful
                booking_check = self.agent.check_booking_success()
                
                if booking_check.get("likely_booking_flow", False):
                    self.current_status = BookingStatus.BOOKING_SUCCESS
                    return BookingResult(
                        status=BookingStatus.BOOKING_SUCCESS,
                        success=True,
                        message="Booking initiated successfully",
                        booked_slot=slot,
                        user_message=f"✅ Successfully initiated booking for {slot.court} on {slot.date} at {slot.time_range}!"
                    )
                else:
                    # Booking may have failed
                    self.current_status = BookingStatus.BOOKING_FAILED
                    return BookingResult(
                        status=BookingStatus.BOOKING_FAILED,
                        success=False,
                        message="Booking attempt did not complete successfully",
                        alternatives=alternatives,
                        user_message="❌ Booking attempt failed. The slot may no longer be available. Here are alternatives if available."
                    )
            else:
                return BookingResult(
                    status=BookingStatus.BOOKING_FAILED,
                    success=False,
                    message=f"Failed to click slot: {click_result.get('message', 'Unknown error')}",
                    alternatives=alternatives,
                    user_message="❌ Could not select the time slot. It may have been booked by someone else."
                )
                
        except Exception as e:
            return BookingResult(
                status=BookingStatus.BOOKING_FAILED,
                success=False,
                message=f"Booking error: {e}",
                user_message="❌ An error occurred while trying to book. Please try again."
            )
    
    def _generate_confirmation_message(self, best_slot: TimeSlot, alternatives: List[TimeSlot]) -> str:
        """Generate user-friendly confirmation message"""
        
        message = f"🎾 Found a great match!\n\n"
        message += f"**Recommended:** {best_slot.court} on {best_slot.date} at {best_slot.time_range}\n\n"
        
        if alternatives:
            message += "**Alternatives:**\n"
            for i, alt in enumerate(alternatives, 1):
                message += f"{i}. {alt.court} at {alt.time_range}\n"
            message += "\n"
        
        message += "Would you like me to book the recommended slot? (yes/no)"
        
        return message

# ============ ENHANCED BOOKING AGENT ============

class EnhancedBookingAgent:
    """Enhanced agent with advanced booking logic"""
    
    def __init__(self, base_agent, use_ai_engine: bool = True):  # Default to using AI
        self.base_agent = base_agent
        self.parser = RequestParser()
        
        # Always try to use AI first
        if hasattr(base_agent, 'model') and base_agent.model:
            print("🤖 Using AI-powered decision engine")
            self.decision_engine = AIDecisionEngine(base_agent.model)
        else:
            print("⚠️ AI model not available, using rule-based engine")
            self.decision_engine = RuleBasedDecisionEngine()
        
        self.workflow = BookingWorkflow(base_agent, self.decision_engine)
    
    def book_court(self, user_request: str) -> BookingResult:
        """Main entry point for booking requests"""
        
        print(f"🎯 Processing booking request: '{user_request}'")
        
        # Parse the request
        parsed_request = self.parser.parse(user_request)
        print(f"📝 Parsed: Date={parsed_request.preferred_date}, Time={parsed_request.preferred_time}, Court={parsed_request.preferred_court}")
        
        # Execute booking workflow
        result = self.workflow.execute_booking(parsed_request)
        
        print(f"🏁 Booking result: {result.status.value} - {result.message}")
        
        return result
    
    def confirm_booking(self, slot: TimeSlot) -> BookingResult:
        """Confirm a specific booking"""
        return self.workflow.confirm_booking(slot)

# ============ TESTING ============

def test_enhanced_booking():
    """Test the enhanced booking system"""
    from badminton_agent import BookingAgent
    
    print("🧪 Testing Enhanced Booking System")
    
    # Create base agent
    base_agent = BookingAgent(headless=False, slow_mo=1000)
    
    # Create enhanced agent
    enhanced_agent = EnhancedBookingAgent(base_agent, use_ai_engine=True)
    
    # Test requests
    test_requests = [
        "Book me a court tomorrow at 7 PM",
        "I need Court #2 today at 9 AM",
        "Find me any available court this afternoon around 3 PM"
    ]
    
    for request in test_requests:
        print(f"\n{'='*50}")
        print(f"Testing: {request}")
        print('='*50)
        
        result = enhanced_agent.book_court(request)
        print(f"\n📊 Result Status: {result.status.value}")
        print(f"💬 User Message: {result.user_message}")
        
        if result.alternatives:
            print(f"🔄 Alternatives: {len(result.alternatives)} options available")
        
        # Cleanup
        time.sleep(2)
    
    # Cleanup
    base_agent.stop_browser()

if __name__ == "__main__":
    test_enhanced_booking()
