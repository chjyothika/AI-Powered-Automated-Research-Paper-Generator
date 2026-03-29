#!/usr/bin/env python3
"""
Generate clean LaTeX paper with all fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ai_generator.generator import AIGenerator

def generate_clean_paper():
    """Generate a clean paper section to test LaTeX fixes"""
    
    topic = 'Disease classification through symptom analysis using machine learning'
    abstract = '''This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases. A symptom-based dataset is used where each record contains a set of symptoms and the corresponding disease, which are converted into numerical values for machine learning processing. After preprocessing, a Random Forest classifier is trained to learn the relationship between symptoms and diseases.'''
    
    print("Generating Clean LaTeX Content")
    print("=" * 40)
    
    generator = AIGenerator()
    
    # Generate methodology section (has equations and formatting)
    content = generator.generate_section('methodology', topic, abstract, [])
    
    print(f"Generated content length: {len(content)} characters")
    
    # Check for LaTeX issues
    issues = []
    if '#' in content and '\\#' not in content:
        issues.append("Unescaped # characters")
    if '\\textbf{' in content and content.count('\\textbf{') != content.count('}'):
        issues.append("Malformed textbf commands")
    if '\\n' in content:
        issues.append("Raw newlines in equations")
    
    if issues:
        print("LaTeX Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No LaTeX issues detected!")
    
    # Save to file for testing
    with open('test_clean.tex', 'w', encoding='utf-8') as f:
        f.write(f"""\\documentclass[conference]{{IEEEtran}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\begin{{document}}
\\section{{Methodology}}
{content}
\\end{{document}}""")
    
    print("Saved test file: test_clean.tex")
    print("Content preview:")
    print(content[:500] + "...")

if __name__ == "__main__":
    generate_clean_paper()