#!/usr/bin/env python3
"""
Test Google AI model availability
"""

import os
import google.generativeai as genai

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def test_google_ai():
    """Test which Google AI models are available"""
    
    print("🔍 Testing Google AI model availability...")
    
    # List available models
    try:
        print("📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"   ✅ {model.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    # Test different model names
    model_names = [
        'gemini-1.5-flash',
        'gemini-1.5-pro', 
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro'
    ]
    
    for model_name in model_names:
        try:
            print(f"\n🧪 Testing model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            # Simple test
            response = model.generate_content("Say hello in one word")
            print(f"   ✅ Success: {response.text.strip()}")
            
            # This model works, we can use it
            return model_name
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    return None

if __name__ == "__main__":
    working_model = test_google_ai()
    if working_model:
        print(f"\n🎉 Working model found: {working_model}")
    else:
        print("\n❌ No working models found")
