#!/usr/bin/env python3
"""
Test adaptive equations and multi-source paper retrieval
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.equation_generator.equations import EquationGenerator
from src.multi_source_fetcher.fetcher import MultiSourceFetcher

def test_adaptive_system():
    """Test adaptive equations for different algorithms"""
    
    print("Testing Adaptive Equation Generation")
    print("=" * 50)
    
    eq_generator = EquationGenerator()
    
    # Test different algorithm types
    test_cases = [
        ("Neural Network Image Classification", "deep learning neural network for image classification using convolutional layers"),
        ("SVM Text Classification", "support vector machine classifier for text classification with RBF kernel"),
        ("K-means Clustering Analysis", "unsupervised learning using k-means clustering algorithm for data segmentation"),
        ("Logistic Regression Prediction", "logistic regression model for binary classification and probability prediction"),
        ("Random Forest Disease Classification", "random forest classifier for disease prediction based on symptoms")
    ]
    
    for topic, abstract in test_cases:
        print(f"\nTopic: {topic}")
        equations = eq_generator.get_relevant_equations(topic, abstract)
        
        if equations:
            print(f"Generated {len(equations)} specific equations:")
            for i, eq in enumerate(equations):
                print(f"  Equation {i+1}: {eq[:60]}...")
        else:
            print("No equations generated")
    
    print("\n" + "=" * 50)
    print("Testing Multi-Source Paper Retrieval")
    print("=" * 50)
    
    fetcher = MultiSourceFetcher()
    
    # Test multi-source retrieval
    query = "machine learning classification"
    papers = fetcher.search_all_sources(query, max_results=20)
    
    print(f"Retrieved {len(papers)} papers from multiple sources")
    
    # Count papers by source
    source_counts = {}
    for paper in papers:
        source_counts[paper.source] = source_counts.get(paper.source, 0) + 1
    
    print("Papers by source:")
    for source, count in source_counts.items():
        print(f"  {source}: {count} papers")
    
    # Show sample papers
    print("\nSample papers:")
    for i, paper in enumerate(papers[:3]):
        print(f"\n{i+1}. {paper.title[:80]}...")
        print(f"   Source: {paper.source}")
        print(f"   Authors: {', '.join(paper.authors[:2])}...")
    
    print("\n" + "=" * 50)
    print("Adaptive System Test Complete")

if __name__ == "__main__":
    test_adaptive_system()