#!/usr/bin/env python3
"""
Test enhanced content generation directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ai_generator.generator import AIGenerator

def test_enhanced_content():
    """Test the enhanced content generation directly"""
    
    generator = AIGenerator()
    
    topic = "Disease Classification Through Symptom Analysis Using Machine Learning"
    user_abstract = """This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases. A symptom-based dataset is used where each record contains a set of symptoms and the corresponding disease, which are converted into numerical values for machine learning processing. After preprocessing, a Random Forest classifier is trained to learn the relationship between symptoms and diseases. The trained model allows users to enter symptoms and predicts the most likely disease, helping users gain an initial understanding of their health condition while supporting medical decision-making."""
    
    print("Testing Enhanced Content Generation")
    print("=" * 50)
    
    sections = ["introduction", "literature_review", "methodology", "results", "conclusion"]
    
    total_length = 0
    total_realistic_indicators = 0
    
    for section in sections:
        print(f"\n{section.upper()}:")
        print("-" * 30)
        
        content = generator.generate_section(section, topic, user_abstract, [])
        
        print(f"Length: {len(content)} characters")
        
        # Check realistic indicators
        indicators = {
            'Percentages': content.count('%'),
            'Numbers': len([x for x in content.split() if any(c.isdigit() for c in x)]),
            'Accuracy': content.lower().count('accuracy'),
            'Dataset': content.lower().count('dataset'),
            'Patients': content.lower().count('patient'),
            'Hospital': content.lower().count('hospital'),
            'Citations': content.count('(') + content.count('['),
        }
        
        section_indicators = sum(indicators.values())
        total_realistic_indicators += section_indicators
        total_length += len(content)
        
        print(f"Realistic indicators: {section_indicators}")
        print(f"Preview: {content[:200]}...")
        
        if len(content) > 1500 and section_indicators > 5:
            print("PASS: REALISTIC CONTENT")
        else:
            print("FAIL: NEEDS IMPROVEMENT")
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Total content length: {total_length} characters")
    print(f"Total realistic indicators: {total_realistic_indicators}")
    
    if total_length > 10000 and total_realistic_indicators > 100:
        print("SUCCESS: Content is highly realistic and detailed!")
    elif total_length > 8000 and total_realistic_indicators > 50:
        print("GOOD: Content is realistic with good detail!")
    else:
        print("ISSUE: Content needs more realistic details")

if __name__ == "__main__":
    test_enhanced_content()