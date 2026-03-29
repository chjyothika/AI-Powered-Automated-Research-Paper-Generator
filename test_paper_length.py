#!/usr/bin/env python3
"""
Test full paper generation with expanded content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ai_generator.generator import AIGenerator

def test_full_paper_length():
    """Test full paper generation with all sections"""
    
    topic = 'Disease classification through symptom analysis using machine learning'
    abstract = '''This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases.'''
    
    print("Testing Full Paper Length")
    print("=" * 40)
    
    generator = AIGenerator()
    sections = ["introduction", "literature_review", "methodology", "results", "conclusion"]
    
    total_length = 0
    for section in sections:
        content = generator.generate_section(section, topic, abstract, [])
        length = len(content)
        total_length += length
        print(f"{section.upper()}: {length} characters")
    
    print(f"\nTOTAL CONTENT: {total_length} characters")
    print(f"Estimated pages: {total_length / 2500:.1f} pages")
    
    if total_length > 15000:
        print("SUCCESS: Paper is long enough (6+ pages)")
    else:
        print("ISSUE: Paper is too short")

if __name__ == "__main__":
    test_full_paper_length()