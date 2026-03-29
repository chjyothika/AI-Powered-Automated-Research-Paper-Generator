#!/usr/bin/env python3
"""
Test enhanced system with implementation-specific content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.equation_generator.equations import EquationGenerator
from src.arxiv_fetcher.fetcher import ArxivFetcher

def test_enhanced_system():
    """Test implementation-specific equations and better paper retrieval"""
    
    topic = 'Disease classification through symptom analysis using machine learning'
    abstract = '''This project presents a machine learning–based disease prediction system that predicts possible diseases based on symptoms provided by the user. The main objective is to assist in early disease identification by analysing common symptoms and mapping them to potential diseases. A symptom-based dataset is used where each record contains a set of symptoms and the corresponding disease, which are converted into numerical values for machine learning processing. After preprocessing, a Random Forest classifier is trained to learn the relationship between symptoms and diseases. The trained model allows users to enter symptoms and predicts the most likely disease, helping users gain an initial understanding of their health condition while supporting medical decision-making.'''
    
    print("Testing Enhanced System")
    print("=" * 50)
    
    # Test 1: Implementation-specific equations
    print("1. Testing Implementation-Specific Equations:")
    eq_generator = EquationGenerator()
    equations = eq_generator.get_relevant_equations(topic, abstract)
    
    if equations:
        print(f"Generated {len(equations)} equations:")
        for i, eq in enumerate(equations):
            print(f"\nEquation {i+1}:")
            print(eq[:100] + "...")
            
            # Check if equations are implementation-specific
            if any(term in eq for term in ['P(D_j|S)', 'Symptom_weight', 'Confidence', 'Random Forest']):
                print("PASS: Implementation-specific equation")
            else:
                print("FAIL: Generic equation")
    else:
        print("FAIL: No equations generated")
    
    # Test 2: Enhanced paper retrieval
    print("\n2. Testing Enhanced Paper Retrieval:")
    fetcher = ArxivFetcher()
    papers = fetcher.search_papers(topic, max_results=15)
    
    print(f"Retrieved {len(papers)} papers")
    
    if len(papers) >= 10:
        print("PASS: Retrieved sufficient papers")
    else:
        print("FAIL: Insufficient papers retrieved")
    
    # Check paper relevance
    relevant_count = 0
    for paper in papers[:5]:
        title_abstract = f"{paper.title} {paper.abstract}".lower()
        if any(term in title_abstract for term in ['disease', 'classification', 'symptom', 'medical', 'diagnosis']):
            relevant_count += 1
    
    if relevant_count >= 3:
        print(f"PASS: {relevant_count}/5 papers are relevant")
    else:
        print(f"FAIL: Only {relevant_count}/5 papers are relevant")
    
    print("\n" + "=" * 50)
    print("Enhanced System Test Complete")

if __name__ == "__main__":
    test_enhanced_system()