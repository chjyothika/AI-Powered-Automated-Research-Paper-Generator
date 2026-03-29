#!/usr/bin/env python3
"""
Debug equation generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.equation_generator.equations import EquationGenerator

def debug_equations():
    """Debug equation generation"""
    
    eq_generator = EquationGenerator()
    
    topic = 'Disease classification using Random Forest'
    abstract = 'machine learning classifier for medical diagnosis using Random Forest algorithm'
    
    print("Debug Equation Generation")
    print("=" * 40)
    print(f"Topic: {topic}")
    print(f"Abstract: {abstract}")
    
    equations = eq_generator.get_relevant_equations(topic, abstract)
    
    print(f"\nGenerated {len(equations)} equations:")
    for i, eq in enumerate(equations):
        print(f"\nEquation {i+1}:")
        print(eq)
        print(f"Contains 'Random Forest': {'Random Forest' in eq}")
        print(f"Contains 'Gini': {'Gini' in eq}")
        print(f"Contains 'P(D_i|S)': {'P(D_i|S)' in eq}")

if __name__ == "__main__":
    debug_equations()