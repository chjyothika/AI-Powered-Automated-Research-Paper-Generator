#!/usr/bin/env python3
"""
Test realistic content generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ollama_generator.ollama_llm import OllamaGenerator

def test_realistic_content():
    """Test the enhanced realistic content generation"""
    
    generator = OllamaGenerator()
    
    topic = "Disease Classification Through Symptom Analysis Using Machine Learning"
    user_abstract = "This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases."
    
    print("Testing Realistic Content Generation")
    print("=" * 50)
    
    sections = ["introduction", "literature_review", "methodology", "results", "conclusion"]
    
    for section in sections:
        print(f"\n{section.upper()}:")
        print("-" * 30)
        
        content = generator.generate_realistic_content(section, topic, user_abstract)
        
        # Check content length and realism
        print(f"Length: {len(content)} characters")
        
        # Look for specific indicators of realistic content
        realistic_indicators = [
            "%" in content,  # Percentages
            any(char.isdigit() for char in content),  # Numbers
            "(" in content and ")" in content,  # Citations or data points
            "accuracy" in content.lower(),  # Performance metrics
            "dataset" in content.lower() or "data" in content.lower(),  # Data references
        ]
        
        realism_score = sum(realistic_indicators)
        print(f"Realism indicators: {realism_score}/5")
        
        # Show first 200 characters
        print(f"Preview: {content[:200]}...")
        
        if len(content) > 1000 and realism_score >= 3:
            print("✓ PASS: Content is realistic and detailed")
        else:
            print("✗ FAIL: Content needs improvement")
    
    print("\n" + "=" * 50)
    print("Realistic Content Generation Test Complete")

if __name__ == "__main__":
    test_realistic_content()