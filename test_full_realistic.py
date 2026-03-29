#!/usr/bin/env python3
"""
Test full realistic paper generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from paper_generator import ResearchPaperGenerator

def test_realistic_paper():
    """Test full paper generation with realistic content"""
    
    topic = 'Disease classification through symptom analysis using machine learning'
    abstract = '''This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases. A symptom-based dataset is used where each record contains a set of symptoms and the corresponding disease, which are converted into numerical values for machine learning processing. After preprocessing, a Random Forest classifier is trained to learn the relationship between symptoms and diseases. The trained model allows users to enter symptoms and predicts the most likely disease, helping users gain an initial understanding of their health condition while supporting medical decision-making.'''
    
    print("Testing Full Realistic Paper Generation")
    print("=" * 60)
    
    generator = ResearchPaperGenerator()
    result = generator.generate_paper(topic, abstract, 'ieee')
    
    print(f"Status: {result.get('success', False)}")
    
    if result['success']:
        content = result['paper_content']
        # Combine all section content
        full_content = ''
        for section, text in content.items():
            full_content += text + ' '
        
        print(f"Total content length: {len(full_content)} characters")
        
        # Check for realistic content indicators
        indicators = {
            'Percentages': full_content.count('%'),
            'Accuracy mentions': full_content.lower().count('accuracy'),
            'Dataset mentions': full_content.lower().count('dataset'),
            'Patient mentions': full_content.lower().count('patient'),
            'Hospital mentions': full_content.lower().count('hospital'),
            'Numbers': len([x for x in full_content.split() if any(c.isdigit() for c in x)]),
            'Citations': full_content.count('(') + full_content.count('['),
        }
        
        print("\nRealistic Content Indicators:")
        for indicator, count in indicators.items():
            print(f"  {indicator}: {count}")
        
        # Check content quality
        total_indicators = sum(indicators.values())
        print(f"\nTotal realistic indicators: {total_indicators}")
        
        if len(full_content) > 8000 and total_indicators > 50:
            print("SUCCESS: Paper contains realistic, detailed research content!")
        else:
            print("ISSUE: Content may need more realistic details")
            
        print(f"\nLaTeX file generated: {result['files']['latex_file']}")
        
        # Show sample from introduction
        intro_content = content.get('introduction', '')
        if intro_content:
            print(f"\nIntroduction sample:\n{intro_content[:500]}...")
            
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_realistic_paper()