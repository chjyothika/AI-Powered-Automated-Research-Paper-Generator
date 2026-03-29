"""
Minimal working test - bypasses ChromaDB issues for now
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_components():
    """Test individual components"""
    print("Testing individual components...")
    
    # Test arXiv fetcher
    try:
        from src.arxiv_fetcher import ArxivFetcher
        fetcher = ArxivFetcher()
        papers = fetcher.search_papers("machine learning", max_results=3)
        print(f"PASS arXiv Fetcher: Found {len(papers)} papers")
        arxiv_ok = len(papers) > 0
    except Exception as e:
        print(f"FAIL arXiv Fetcher failed: {e}")
        arxiv_ok = False
    
    # Test AI Generator
    try:
        from src.ai_generator import AIGenerator
        generator = AIGenerator()
        content = generator.generate_section("introduction", "machine learning")
        print(f"PASS AI Generator: Generated {len(content)} characters")
        ai_ok = len(content) > 50
    except Exception as e:
        print(f"FAIL AI Generator failed: {e}")
        ai_ok = False
    
    # Test LaTeX Templates
    try:
        from src.latex_templates import LaTeXTemplateManager
        manager = LaTeXTemplateManager()
        template = manager.generate_template("ieee", "Test Paper", "Test Author", "Test abstract")
        print(f"PASS LaTeX Templates: Generated {len(template)} characters")
        latex_ok = len(template) > 100
    except Exception as e:
        print(f"FAIL LaTeX Templates failed: {e}")
        latex_ok = False
    
    # Test Citation Engine
    try:
        from src.citation_engine import CitationEngine
        engine = CitationEngine()
        paper_data = {
            'metadata': {
                'title': 'Test Paper',
                'authors': 'Test Author',
                'published': '2023-01-01',
                'arxiv_id': '2301.12345'
            }
        }
        citation_key = engine.add_paper_citation(paper_data)
        bibtex = engine.generate_bibtex_entry(citation_key)
        print(f"PASS Citation Engine: Generated citation")
        citation_ok = len(bibtex) > 50
    except Exception as e:
        print(f"FAIL Citation Engine failed: {e}")
        citation_ok = False
    
    return arxiv_ok, ai_ok, latex_ok, citation_ok

def test_minimal_paper_generation():
    """Test minimal paper generation without RAG"""
    print("\nTesting minimal paper generation...")
    
    try:
        from src.arxiv_fetcher import ArxivFetcher
        from src.ai_generator import AIGenerator
        from src.latex_templates import LaTeXTemplateManager
        from src.citation_engine import CitationEngine
        
        # Get some papers
        fetcher = ArxivFetcher()
        papers = fetcher.search_papers("machine learning", max_results=3)
        
        if not papers:
            print("FAIL No papers found")
            return False
        
        # Generate content
        generator = AIGenerator()
        sections = {}
        
        for section in ["abstract", "introduction", "conclusion"]:
            content = generator.generate_section(section, "machine learning")
            sections[section] = content
            print(f"PASS Generated {section}: {len(content)} chars")
        
        # Create LaTeX
        template_manager = LaTeXTemplateManager()
        template = template_manager.generate_template(
            "ieee", 
            "AI-Generated Paper on Machine Learning",
            "Test Author",
            sections["abstract"]
        )
        
        # Add sections
        content_parts = []
        for section in ["introduction", "conclusion"]:
            if section in sections:
                formatted = template_manager.format_section(section, sections[section], "ieee")
                content_parts.append(formatted)
        
        final_latex = template.replace("{CONTENT}", "\n".join(content_parts))
        final_latex = final_latex.replace("{BIBLIOGRAPHY}", "% Bibliography would go here")
        
        # Save file
        output_file = os.path.join("output", "test_paper.tex")
        os.makedirs("output", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_latex)
        
        print(f"PASS Paper generated: {output_file}")
        print(f"PASS File size: {len(final_latex)} characters")
        
        return True
        
    except Exception as e:
        print(f"FAIL Paper generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("AI Research Paper Generator - Minimal Test")
    print("=" * 50)
    
    # Test components
    arxiv_ok, ai_ok, latex_ok, citation_ok = test_components()
    
    # Test paper generation if core components work
    if arxiv_ok and ai_ok and latex_ok:
        paper_ok = test_minimal_paper_generation()
    else:
        paper_ok = False
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print(f"arXiv Fetcher:     {'PASS' if arxiv_ok else 'FAIL'}")
    print(f"AI Generator:      {'PASS' if ai_ok else 'FAIL'}")
    print(f"LaTeX Templates:   {'PASS' if latex_ok else 'FAIL'}")
    print(f"Citation Engine:   {'PASS' if citation_ok else 'FAIL'}")
    print(f"Paper Generation:  {'PASS' if paper_ok else 'FAIL'}")
    
    all_ok = all([arxiv_ok, ai_ok, latex_ok, citation_ok, paper_ok])
    
    if all_ok:
        print("\nSUCCESS: Core system is working!")
        print("\nNext steps:")
        print("1. Fix ChromaDB issues for full RAG functionality")
        print("2. Start web interface: streamlit run app.py")
        print("3. Check generated paper in output/test_paper.tex")
    else:
        print("\nSome components failed - check errors above")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)