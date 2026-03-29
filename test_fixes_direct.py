#!/usr/bin/env python3
"""
Test template generation and equation fixes directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.latex_templates.template_manager import LaTeXTemplateManager
from src.equation_generator.equations import EquationGenerator
from src.ai_generator.generator import AIGenerator

def test_fixes():
    """Test the specific fixes"""
    
    print("Testing All Fixes")
    print("=" * 40)
    
    # Test 1: Keywords
    print("1. Testing Keywords Generation:")
    template_manager = LaTeXTemplateManager()
    keywords = ['machine learning', 'disease classification', 'symptom analysis', 'medical diagnosis', 'healthcare']
    
    template = template_manager.generate_template(
        publisher='ieee',
        title='Disease Classification Through Symptom Analysis',
        authors='Research Author',
        abstract='This project presents a machine learning system...',
        keywords=keywords
    )
    
    if template:
        if 'machine learning, disease classification' in template:
            print("  PASS: Realistic keywords generated")
        else:
            print("  FAIL: Keywords not properly inserted")
        
        if 'keyword1, keyword2' not in template:
            print("  PASS: No generic keywords")
        else:
            print("  FAIL: Still contains generic keywords")
    
    # Test 2: Equations
    print("\n2. Testing Equation Generation:")
    eq_generator = EquationGenerator()
    equations = eq_generator.get_relevant_equations(
        'Disease classification using Random Forest',
        'machine learning classifier for medical diagnosis'
    )
    
    if equations:
        print(f"  PASS: Generated {len(equations)} relevant equations")
        for i, eq in enumerate(equations):
            if ('Random Forest' in eq or 'Gini' in eq or 'P(D_i|S)' in eq or 
                'T_b(x)' in eq or 'IG(S,A)' in eq or 'H(S)' in eq):
                print(f"  PASS: Equation {i+1} is topic-specific")
            else:
                print(f"  FAIL: Equation {i+1} is generic")
    else:
        print("  FAIL: No equations generated")
    
    # Test 3: Content formatting
    print("\n3. Testing Content Formatting:")
    ai_generator = AIGenerator()
    content = ai_generator.generate_section(
        'methodology',
        'Disease classification through symptom analysis using machine learning',
        'This project presents a machine learning system for disease prediction',
        []
    )
    
    if '\\textbf{' in content:
        print("  PASS: LaTeX bold formatting used")
    else:
        print("  FAIL: No LaTeX bold formatting found")
    
    if '**' not in content:
        print("  PASS: No markdown formatting")
    else:
        print("  FAIL: Still contains markdown formatting")
    
    print(f"\nContent length: {len(content)} characters")
    if len(content) > 2000:
        print("  PASS: Content is detailed")
    else:
        print("  FAIL: Content too short")
    
    print("\n" + "=" * 40)
    print("Fix Testing Complete")

if __name__ == "__main__":
    test_fixes()