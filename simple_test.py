"""
Simple test script for the Research Paper Generator
Tests core functionality without Unicode characters
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_arxiv_simple():
    """Simple test of arXiv fetcher"""
    print("Testing arXiv fetcher...")
    
    try:
        from src.arxiv_fetcher import ArxivFetcher
        
        fetcher = ArxivFetcher()
        papers = fetcher.search_papers("neural networks", max_results=3)
        
        print(f"SUCCESS: Found {len(papers)} papers")
        
        if papers:
            paper = papers[0]
            print(f"Sample paper: {paper.title[:50]}...")
            print(f"Authors: {len(paper.authors)} authors")
            return True
        else:
            print("WARNING: No papers found")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_full_pipeline_simple():
    """Simple test of full pipeline"""
    print("\nTesting full pipeline...")
    
    try:
        from paper_generator import ResearchPaperGenerator
        
        generator = ResearchPaperGenerator()
        print("SUCCESS: Generator initialized")
        
        # Test with minimal settings
        result = generator.generate_paper(
            topic="machine learning",
            publisher="ieee",
            paper_type="research",
            max_references=3,  # Small number for testing
            author_name="Test Author"
        )
        
        if result.get("success"):
            print("SUCCESS: Paper generated!")
            print(f"Title: {result['title']}")
            print(f"Sections: {result['sections_generated']}")
            print(f"References: {result['references_used']}")
            
            # Check if file exists
            latex_file = result['files']['latex_file']
            if os.path.exists(latex_file):
                print(f"SUCCESS: LaTeX file created: {latex_file}")
                return True
            else:
                print("ERROR: LaTeX file not found")
                return False
        else:
            print(f"ERROR: Paper generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run simple tests"""
    print("AI Research Paper Generator - Simple Test")
    print("=" * 50)
    
    # Test arXiv
    arxiv_ok = test_arxiv_simple()
    
    # Test full pipeline if arXiv works
    if arxiv_ok:
        pipeline_ok = test_full_pipeline_simple()
    else:
        pipeline_ok = False
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"arXiv Fetcher: {'PASS' if arxiv_ok else 'FAIL'}")
    print(f"Full Pipeline: {'PASS' if pipeline_ok else 'FAIL'}")
    
    if arxiv_ok and pipeline_ok:
        print("\nSUCCESS: System is working!")
        print("\nTo start the web interface:")
        print("streamlit run app.py")
    else:
        print("\nSome tests failed. Check the errors above.")
    
    return arxiv_ok and pipeline_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)