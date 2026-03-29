"""
Comprehensive test script for the Research Paper Generator
Tests all components individually and the complete pipeline
"""
import sys
import os
import logging
import traceback
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    try:
        # Test configuration
        import config
        print("✅ Config imported successfully")
        print(f"   Device: {config.DEVICE}")
        print(f"   Supported publishers: {len(config.SUPPORTED_PUBLISHERS)}")
        
        # Test arXiv fetcher
        from src.arxiv_fetcher import ArxivFetcher, ArxivPaper
        print("✅ arXiv fetcher imported successfully")
        
        # Test RAG engine
        from src.rag_engine import RAGEngine
        print("✅ RAG engine imported successfully")
        
        # Test AI generator
        from src.ai_generator import AIGenerator
        print("✅ AI generator imported successfully")
        
        # Test LaTeX templates
        from src.latex_templates import LaTeXTemplateManager
        print("✅ LaTeX templates imported successfully")
        
        # Test citation engine
        from src.citation_engine import CitationEngine
        print("✅ Citation engine imported successfully")
        
        # Test main generator
        from paper_generator import ResearchPaperGenerator
        print("✅ Main paper generator imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_arxiv_fetcher():
    """Test arXiv fetcher functionality"""
    print("\n" + "=" * 60)
    print("TESTING ARXIV FETCHER")
    print("=" * 60)
    
    try:
        from src.arxiv_fetcher import ArxivFetcher
        
        fetcher = ArxivFetcher()
        print("✅ ArxivFetcher initialized")
        
        # Test search
        papers = fetcher.search_papers("machine learning", max_results=3)
        print(f"✅ Search completed: {len(papers)} papers found")
        
        if papers:
            paper = papers[0]
            print(f"   Sample paper: {paper.title[:50]}...")
            print(f"   Authors: {len(paper.authors)} authors")
            print(f"   Abstract length: {len(paper.abstract)} chars")
            print(f"   arXiv ID: {paper.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ arXiv fetcher test failed: {e}")
        traceback.print_exc()
        return False

def test_rag_engine():
    """Test RAG engine functionality"""
    print("\n" + "=" * 60)
    print("TESTING RAG ENGINE")
    print("=" * 60)
    
    try:
        from src.rag_engine import RAGEngine
        from src.arxiv_fetcher import ArxivFetcher
        
        # Initialize components
        rag = RAGEngine()
        print("✅ RAGEngine initialized")
        
        fetcher = ArxivFetcher()
        papers = fetcher.search_papers("neural networks", max_results=3)
        
        if papers:
            # Add papers to RAG
            added = rag.add_papers(papers)
            print(f"✅ Added {added} papers to RAG database")
            
            # Test search
            similar = rag.search_similar_papers("deep learning", top_k=2)
            print(f"✅ Found {len(similar)} similar papers")
            
            # Test stats
            stats = rag.get_collection_stats()
            print(f"✅ RAG stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG engine test failed: {e}")
        traceback.print_exc()
        return False

def test_ai_generator():
    """Test AI generator functionality"""
    print("\n" + "=" * 60)
    print("TESTING AI GENERATOR")
    print("=" * 60)
    
    try:
        from src.ai_generator import AIGenerator
        
        generator = AIGenerator()
        print("✅ AIGenerator initialized")
        
        # Test model info
        info = generator.get_model_info()
        print(f"✅ Model info: {info}")
        
        # Test section generation
        content = generator.generate_section(
            section="introduction",
            topic="machine learning",
            retrieved_papers=[]
        )
        
        print(f"✅ Generated introduction: {len(content)} characters")
        print(f"   Preview: {content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI generator test failed: {e}")
        traceback.print_exc()
        return False

def test_latex_templates():
    """Test LaTeX template manager"""
    print("\n" + "=" * 60)
    print("TESTING LATEX TEMPLATES")
    print("=" * 60)
    
    try:
        from src.latex_templates import LaTeXTemplateManager
        
        manager = LaTeXTemplateManager()
        print("✅ LaTeXTemplateManager initialized")
        
        # Test template generation
        template = manager.generate_template(
            publisher="ieee",
            title="Test Paper",
            authors="Test Author",
            abstract="This is a test abstract."
        )
        
        if template:
            print("✅ IEEE template generated successfully")
            print(f"   Template length: {len(template)} characters")
        
        # Test section formatting
        section = manager.format_section(
            section_name="introduction",
            content="This is test content.",
            publisher="ieee"
        )
        
        print("✅ Section formatting works")
        print(f"   Formatted section: {section[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ LaTeX templates test failed: {e}")
        traceback.print_exc()
        return False

def test_citation_engine():
    """Test citation engine functionality"""
    print("\n" + "=" * 60)
    print("TESTING CITATION ENGINE")
    print("=" * 60)
    
    try:
        from src.citation_engine import CitationEngine
        
        engine = CitationEngine("numeric")
        print("✅ CitationEngine initialized")
        
        # Test paper data
        paper_data = {
            'metadata': {
                'title': 'Test Paper on Machine Learning',
                'authors': 'Smith, John; Doe, Jane',
                'published': '2023-01-15T10:30:00Z',
                'arxiv_id': '2301.12345',
                'categories': 'cs.LG'
            }
        }
        
        # Add citation
        citation_key = engine.add_paper_citation(paper_data)
        print(f"✅ Citation added: {citation_key}")
        
        # Generate BibTeX
        bibtex = engine.generate_bibtex_entry(citation_key)
        print("✅ BibTeX entry generated")
        print(f"   Length: {len(bibtex)} characters")
        
        # Test in-text citation
        in_text = engine.format_in_text_citation([citation_key], "ieee")
        print(f"✅ In-text citation: {in_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Citation engine test failed: {e}")
        traceback.print_exc()
        return False

def test_full_pipeline():
    """Test the complete paper generation pipeline"""
    print("\n" + "=" * 60)
    print("TESTING FULL PIPELINE")
    print("=" * 60)
    
    try:
        from paper_generator import ResearchPaperGenerator
        
        generator = ResearchPaperGenerator()
        print("✅ ResearchPaperGenerator initialized")
        
        # Test system status
        status = generator.get_system_status()
        print(f"✅ System status retrieved: {len(status)} components")
        
        # Test paper generation (with minimal settings for speed)
        print("🚀 Starting paper generation test...")
        
        result = generator.generate_paper(
            topic="neural networks",
            publisher="ieee",
            paper_type="research",
            max_references=5,  # Small number for testing
            author_name="Test Author",
            author_email="test@example.com"
        )
        
        if result.get("success"):
            print("✅ Paper generation successful!")
            print(f"   Title: {result['title']}")
            print(f"   Sections: {result['sections_generated']}")
            print(f"   References: {result['references_used']}")
            print(f"   LaTeX file: {result['files']['latex_file']}")
            
            # Check if files exist
            latex_file = result['files']['latex_file']
            if os.path.exists(latex_file):
                print("✅ LaTeX file created successfully")
                
                # Check file size
                file_size = os.path.getsize(latex_file)
                print(f"   File size: {file_size} bytes")
            else:
                print("❌ LaTeX file not found")
                return False
        else:
            print(f"❌ Paper generation failed: {result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("STARTING COMPREHENSIVE TESTS")
    print("=" * 80)
    
    test_results = {}
    
    # Run individual tests
    test_results["imports"] = test_imports()
    test_results["arxiv_fetcher"] = test_arxiv_fetcher()
    test_results["rag_engine"] = test_rag_engine()
    test_results["ai_generator"] = test_ai_generator()
    test_results["latex_templates"] = test_latex_templates()
    test_results["citation_engine"] = test_citation_engine()
    test_results["full_pipeline"] = test_full_pipeline()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<20} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("ALL TESTS PASSED! System is ready for use.")
    else:
        print("Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)