#!/usr/bin/env python3
"""
Badminton Court Booking Agent - Setup Script
============================================

This script automates the setup process for the Badminton Court Booking Agent.
It handles virtual environment creation, dependency installation, and initial
configuration to get the system running quickly.

Usage:
    python setup.py

Features:
- Creates isolated Python virtual environment
- Installs all required dependencies
- Sets up Playwright browsers
- Validates Google AI API key
- Runs initial system tests
- Provides helpful setup instructions

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def print_header():
    """Print a welcome header for the setup process."""
    print("=" * 60)
    print("🏸 Badminton Court Booking Agent - Setup Script")
    print("=" * 60)
    print("This script will set up your development environment for the")
    print("Badminton Court Booking Agent system.")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment for the project."""
    print("\n📦 Creating virtual environment...")
    
    venv_path = Path("badminton_agent_env")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists. Skipping creation.")
        return True
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def get_activation_command():
    """Get the correct activation command for the current platform."""
    if platform.system() == "Windows":
        return "badminton_agent_env\\Scripts\\activate"
    else:
        return "source badminton_agent_env/bin/activate"

def install_dependencies():
    """Install required Python packages."""
    print("\n📚 Installing dependencies...")
    
    # Determine the correct pip path
    if platform.system() == "Windows":
        pip_path = "badminton_agent_env\\Scripts\\pip"
    else:
        pip_path = "badminton_agent_env/bin/pip"
    
    try:
        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def install_playwright_browsers():
    """Install Playwright browsers."""
    print("\n🌐 Installing Playwright browsers...")
    
    # Determine the correct playwright path
    if platform.system() == "Windows":
        playwright_path = "badminton_agent_env\\Scripts\\playwright"
    else:
        playwright_path = "badminton_agent_env/bin/playwright"
    
    try:
        subprocess.run([playwright_path, "install", "chromium"], check=True)
        print("✅ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Playwright browsers: {e}")
        return False

def check_google_api_key():
    """Check if Google API key is configured."""
    print("\n🔑 Checking Google API key...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  Google API key not found in environment variables.")
        print("   Please set your API key:")
        print("   export GOOGLE_API_KEY='your_api_key_here'")
        print("   Or create a .env file with: GOOGLE_API_KEY=your_api_key_here")
        return False
    
    print("✅ Google API key is configured")
    return True

def run_tests():
    """Run basic system tests."""
    print("\n🧪 Running system tests...")
    
    try:
        # Test basic imports
        sys.path.insert(0, str(Path.cwd()))
        
        # Test badminton_agent import
        from badminton_agent import BookingAgent
        print("✅ BadmintonAgent import successful")
        
        # Test booking_engine import
        from booking_engine import EnhancedBookingAgent
        print("✅ EnhancedBookingAgent import successful")
        
        # Test basic agent creation
        agent = BookingAgent(headless=True)
        print("✅ Agent creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Activate the virtual environment:")
    print(f"   {get_activation_command()}")
    print()
    print("2. Set your Google API key (if not already set):")
    print("   export GOOGLE_API_KEY='your_api_key_here'")
    print()
    print("3. Run the Streamlit interface:")
    print("   streamlit run app.py")
    print()
    print("4. Open your browser to:")
    print("   http://localhost:8502")
    print()
    print("5. Test the system with requests like:")
    print("   - 'What courts are available tomorrow?'")
    print("   - 'Book Court #3 on September 10th at 2 PM'")
    print()
    print("For more information, see README.md")
    print("=" * 60)

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        sys.exit(1)
    
    # Check Google API key
    check_google_api_key()  # Non-fatal, just a warning
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup may still work.")
        print("   Try running the application and check for errors.")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
