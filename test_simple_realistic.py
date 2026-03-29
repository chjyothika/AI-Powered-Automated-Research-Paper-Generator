#!/usr/bin/env python3
"""
Test realistic content generation - simplified
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ollama_generator.ollama_llm import OllamaGenerator

def test_realistic_content():
    """Test the enhanced realistic content generation"""
    
    generator = OllamaGenerator()
    
    topic = "Disease Classification Through Symptom Analysis Using Machine Learning"
    user_abstract = "This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user."
    
    print("Testing Realistic Content Generation")
    print("=" * 50)
    
    # Test introduction section
    content = generator.generate_realistic_content("introduction", topic, user_abstract)
    
    print(f"Content Length: {len(content)} characters")
    print(f"Contains percentages: {'%' in content}")
    print(f"Contains numbers: {any(char.isdigit() for char in content)}")
    print(f"Contains citations: {'(' in content and ')' in content}")
    print(f"Contains accuracy metrics: {'accuracy' in content.lower()}")
    
    print("\nFirst 500 characters:")
    print(content[:500])
    
    print("\n" + "=" * 50)
    if len(content) > 1500:
        print("SUCCESS: Content is detailed and realistic!")
    else:
        print("ISSUE: Content may be too short")

if __name__ == "__main__":
    test_realistic_content()