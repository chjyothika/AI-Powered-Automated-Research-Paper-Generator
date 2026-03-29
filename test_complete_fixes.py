#!/usr/bin/env python3
"""
Test the complete enhanced system with all fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from paper_generator import ResearchPaperGenerator

def test_complete_system():
    """Test the complete enhanced system"""
    
    topic = 'Disease classification through symptom analysis using machine learning'
    abstract = '''This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases. A symptom-based dataset is used where each record contains a set of symptoms and the corresponding disease, which are converted into numerical values for machine learning processing. After preprocessing, a Random Forest classifier is trained to learn the relationship between symptoms and diseases. The trained model allows users to enter symptoms and predicts the most likely disease, helping users gain an initial understanding of their health condition while supporting medical decision-making.'''
    
    print("Testing Complete Enhanced System")
    print("=" * 50)
    
    try:
        generator = ResearchPaperGenerator()
        result = generator.generate_paper(topic, abstract, 'ieee')
        
        if result.get('success'):
            print("SUCCESS: Paper generated successfully!")
            print(f"Title: {result['title']}")
            print(f"LaTeX file: {result['files']['latex_file']}")
            
            # Read and check the generated LaTeX file
            with open(result['files']['latex_file'], 'r', encoding='utf-8') as f:
                latex_content = f.read()
            
            # Check for fixes
            fixes_check = {
                'Realistic Keywords': 'machine learning, disease classification' in latex_content,
                'No Generic Keywords': 'keyword1, keyword2' not in latex_content,
                'Proper LaTeX Bold': '\\textbf{' in latex_content,
                'No Markdown Bold': '**' not in latex_content,
                'Specific Equations': 'Random Forest ensemble' in latex_content or 'Gini impurity' in latex_content,
                'No Generic Equations': 'core mathematical formulation of our approach' not in latex_content,
                'Realistic Content': len(latex_content) > 15000
            }
            
            print("\nFixes Verification:")
            for fix, status in fixes_check.items():
                status_text = "PASS" if status else "FAIL"
                print(f"  {fix}: {status_text}")
            
            all_passed = all(fixes_check.values())
            print(f"\nOverall Status: {'ALL FIXES APPLIED' if all_passed else 'SOME ISSUES REMAIN'}")
            
            # Show sample of keywords section
            if '\\begin{IEEEkeywords}' in latex_content:
                start = latex_content.find('\\begin{IEEEkeywords}')
                end = latex_content.find('\\end{IEEEkeywords}', start) + len('\\end{IEEEkeywords}')
                keywords_section = latex_content[start:end]
                print(f"\nKeywords Section:\n{keywords_section}")
            
        else:
            print(f"FAILED: {result.get('error')}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_complete_system()