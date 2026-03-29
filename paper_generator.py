"""
Main Paper Generator - Orchestrates the complete research paper generation pipeline
Coordinates arXiv fetching, RAG retrieval, AI generation, and LaTeX assembly
"""
import os
import logging
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from config import OUTPUT_DIR, PAPER_SECTIONS, SUPPORTED_PUBLISHERS, LATEX_COMPILE, PDFLATEX_PATH, MIN_REFERENCES, MAX_REFERENCES, TARGET_PAPER_LENGTH
from src.multi_source_fetcher import MultiSourceFetcher
from src.rag_engine import RAGEngine
from src.ai_generator import AIGenerator
from src.latex_templates import LaTeXTemplateManager
from src.citation_engine import CitationEngine
from src.graph_generator import GraphResultsGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchPaperGenerator:
    """
    Main orchestrator for AI-powered research paper generation
    Coordinates all components to produce publication-ready papers
    """
    
    def __init__(self):
        # Initialize all components
        logger.info("Initializing Research Paper Generator...")
        
        self.multi_fetcher = MultiSourceFetcher()
        self.rag_engine = RAGEngine()
        self.ai_generator = AIGenerator()
        self.template_manager = LaTeXTemplateManager()
        self.graph_generator = GraphResultsGenerator()
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        logger.info("All components initialized successfully")
    
    def generate_paper(
        self,
        topic: str,
        user_abstract: str,
        publisher: str = "ieee",
        paper_type: str = "research",
        max_references: int = 20,
        author_name: str = "Research Author",
        author_email: str = "author@institution.edu",
        authors: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a complete research paper
        
        Args:
            topic: Research topic/title
            user_abstract: User-provided abstract (semantic anchor)
            publisher: Target publisher (ieee, elsevier, acm, springer)
            paper_type: Type of paper (research, review, survey)
            max_references: Maximum number of references to include
            author_name: Author name for the paper
            author_email: Author email
            
        Returns:
            Dictionary containing generated paper data and file paths
        """
        try:
            logger.info(f"Starting paper generation for topic: {topic}")
            logger.info(f"Publisher: {publisher}, Type: {paper_type}")
            
            # Step 1: Calculate dynamic reference count based on topic complexity
            dynamic_ref_count = self._calculate_reference_count(topic, user_abstract, max_references)
            logger.info(f"Dynamic reference count: {dynamic_ref_count}")
            
            # Step 2: Extract keywords from title and abstract for better search
            logger.info("Step 2: Extracting search keywords...")
            search_keywords = self._extract_search_keywords(topic, user_abstract)
            logger.info(f"Search keywords: {search_keywords}")
            
            # Step 3: Fetch relevant papers from multiple sources
            logger.info("Step 3: Fetching papers from multiple sources...")
            academic_papers = self.multi_fetcher.search_all_sources(search_keywords, max_results=dynamic_ref_count)
            
            if not academic_papers:
                logger.warning("No papers found from any source for this topic")
                return {"error": "No relevant papers found from academic sources"}
            
            logger.info(f"Found {len(academic_papers)} papers from multiple sources")
            
            # Step 4: Store papers in RAG database (clear stale data first)
            logger.info("Step 4: Building RAG database...")
            try:
                self.rag_engine.clear_collection()
            except Exception:
                pass  # OK if collection didn't exist
            added_count = self.rag_engine.add_papers(academic_papers)
            logger.info(f"Added {added_count} papers to RAG database")
            
            # Step 5: Retrieve most relevant papers using topic + abstract
            logger.info("Step 5: Retrieving relevant papers...")
            search_context = f"{topic}. {user_abstract}"
            relevant_papers = self.rag_engine.search_similar_papers(search_context, top_k=min(15, len(academic_papers)))
            
            # Step 6: Initialize citation engine
            citation_style = self.template_manager.get_citation_style(publisher)
            citation_engine = CitationEngine(citation_style)
            
            # Step 7: Generate paper sections
            logger.info("Step 7: Generating paper content...")
            paper_content = {}
            citation_keys_by_section = {}
            
            # Extract keywords from topic and abstract
            keywords = self._extract_keywords_from_content(topic, user_abstract)
            
            for section in PAPER_SECTIONS:
                logger.info(f"Generating {section} section...")
                
                # Generate section content with abstract consistency
                content = self.ai_generator.generate_section(
                    section=section,
                    topic=topic,
                    user_abstract=user_abstract,
                    retrieved_papers=relevant_papers
                )
                
                # Insert citations if not abstract
                if section != "abstract":
                    # Use different papers for different sections
                    section_papers = self._get_section_papers(section, relevant_papers)
                    content_with_citations, citation_keys = citation_engine.insert_citations_in_text(
                        content, section_papers, publisher, section_name=section
                    )
                    paper_content[section] = content_with_citations
                    citation_keys_by_section[section] = citation_keys
                else:
                    # Use user-provided abstract
                    paper_content[section] = user_abstract
                    citation_keys_by_section[section] = []
            
            # Step 8: Generate figures for the results section
            logger.info("Step 8: Generating figures...")
            figures = []
            try:
                figures = self.graph_generator.generate_all_figures(topic, OUTPUT_DIR)
                logger.info(f"Generated {len(figures)} figures")
            except Exception as e:
                logger.warning(f"Figure generation failed (non-fatal): {e}")

            # Insert figure references into results section
            if figures and "results" in paper_content:
                figure_latex = "\n\n"
                for fig in figures:
                    figure_latex += f"""\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.45\\textwidth]{{{fig['path']}}}
\\caption{{{fig['caption']}}}
\\label{{{fig['label']}}}
\\end{{figure}}\n\n"""
                paper_content["results"] = paper_content["results"] + figure_latex

            # Step 8b: Generate paper title
            paper_title = self._generate_paper_title(topic, paper_type)
            
            # Resolve authors: prefer the structured list, fallback to name string
            if not authors:
                authors = [{"name": author_name, "email": author_email,
                            "institution": "Research Institution",
                            "department": "Department",
                            "city": "City", "country": "Country"}]

            # Step 9: Assemble LaTeX document
            logger.info("Step 9: Assembling LaTeX document...")
            latex_content = self._assemble_latex_document(
                paper_content=paper_content,
                title=paper_title,
                authors=authors,
                publisher=publisher,
                citation_engine=citation_engine,
                keywords=keywords
            )
            
            # Step 10: Generate bibliography
            logger.info("Step 10: Generating bibliography...")
            if publisher.lower() in ["acm"]:
                # Use BibTeX
                bibliography = citation_engine.generate_full_bibliography()
                bib_filename = self._save_bibliography(bibliography, topic)
            else:
                # Use LaTeX bibliography
                bibliography = citation_engine.generate_latex_bibliography(publisher)
                bib_filename = None
            
            # Step 11: Save files
            logger.info("Step 11: Saving generated files...")
            tex_filename = self._save_latex_file(latex_content, topic, publisher)
            
            # Step 12: Compile PDF if enabled
            pdf_filename = None
            if LATEX_COMPILE:
                logger.info("Step 12: Compiling PDF...")
                pdf_filename = self._compile_pdf(tex_filename)
            
            # Generate summary
            result = {
                "success": True,
                "topic": topic,
                "user_abstract": user_abstract,
                "publisher": publisher,
                "paper_type": paper_type,
                "title": paper_title,
                "author": authors[0]["name"] if authors else author_name,
                "sections_generated": len(paper_content),
                "references_found": len(academic_papers),
                "references_used": len(citation_engine.citations),
                "files": {
                    "latex_file": tex_filename,
                    "bibliography_file": bib_filename,
                    "pdf_file": pdf_filename
                },
                "generation_time": datetime.now().isoformat(),
                "paper_content": paper_content,
                "citations": citation_engine.get_citation_stats()
            }
            
            logger.info("Paper generation completed successfully!")
            return result
            
        except Exception as e:
            logger.error(f"Paper generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "topic": topic,
                "publisher": publisher
            }
    
    def _extract_search_keywords(self, topic: str, abstract: str) -> str:
        """Extract relevant keywords from title and abstract for better arXiv search"""
        import re
        
        # Combine topic and abstract
        text = f"{topic}. {abstract}".lower()
        
        # Remove common stop words and extract meaningful terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        # Extract important technical terms
        important_patterns = [
            r'machine learning', r'deep learning', r'neural network', r'artificial intelligence',
            r'classification', r'prediction', r'regression', r'clustering', r'optimization',
            r'algorithm', r'model', r'framework', r'system', r'method', r'approach',
            r'analysis', r'detection', r'recognition', r'processing', r'mining'
        ]
        
        keywords = []
        
        # Add multi-word technical terms
        for pattern in important_patterns:
            if re.search(pattern, text):
                keywords.append(pattern.replace(' ', '+'))
        
        # Add individual important words
        words = re.findall(r'\b[a-z]{4,}\b', text)
        important_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Take most frequent important words
        word_freq = {}
        for word in important_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and take top words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords.extend([word for word, freq in top_words])
        
        # Create search query
        search_query = ' OR '.join(keywords[:8])  # Limit to 8 terms
        return search_query if search_query else topic
    
    def _calculate_reference_count(self, topic: str, abstract: str, max_requested: int) -> int:
        """Calculate dynamic reference count based on topic complexity"""
        # Base reference count
        base_count = MIN_REFERENCES
        
        # Increase based on abstract length (longer abstracts = more complex topics)
        abstract_words = len(abstract.split())
        if abstract_words > 150:
            base_count += 10
        elif abstract_words > 100:
            base_count += 5
        
        # Increase based on topic complexity indicators
        complexity_keywords = [
            "comprehensive", "novel", "advanced", "complex", "multi", 
            "framework", "system", "architecture", "methodology"
        ]
        
        text = f"{topic} {abstract}".lower()
        complexity_score = sum(1 for keyword in complexity_keywords if keyword in text)
        base_count += complexity_score * 3
        
        # Ensure within bounds
        final_count = min(max(base_count, MIN_REFERENCES), min(max_requested, MAX_REFERENCES))
        return final_count
    
    def _get_section_papers(self, section: str, all_papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get relevant papers for a specific section - use generous amounts"""
        n = len(all_papers)
        section_paper_map = {
            "introduction": all_papers[:min(8, n)],
            "literature_review": all_papers[:n],  # Literature review uses ALL papers
            "methodology": all_papers[2:min(10, n)],
            "results": all_papers[1:min(8, n)],
            "conclusion": all_papers[:min(6, n)]
        }

        return section_paper_map.get(section, all_papers[:min(6, n)])
    
    def _generate_paper_title(self, topic: str, paper_type: str) -> str:
        """Generate an appropriate paper title"""
        type_prefixes = {
            "research": "A Novel Approach to",
            "review": "A Comprehensive Review of",
            "survey": "A Survey on"
        }
        
        prefix = type_prefixes.get(paper_type, "Research on")
        
        # Capitalize topic appropriately
        title_topic = topic.title()
        
        return f"{prefix} {title_topic}: Methods and Applications"
    
    def _assemble_latex_document(
        self,
        paper_content: Dict[str, str],
        title: str,
        authors,
        publisher: str,
        citation_engine: CitationEngine,
        keywords: List[str] = None
    ) -> str:
        """Assemble the complete LaTeX document"""

        # Generate base template
        template = self.template_manager.generate_template(
            publisher=publisher,
            title=title,
            authors=authors,
            abstract=paper_content.get("abstract", ""),
            keywords=keywords
        )
        
        if not template:
            raise ValueError(f"Failed to generate template for publisher: {publisher}")
        
        # Assemble section content
        sections_latex = []
        
        for section in PAPER_SECTIONS:
            if section == "abstract":
                continue  # Already in template
            
            if section in paper_content:
                section_latex = self.template_manager.format_section(
                    section_name=section,
                    content=paper_content[section],
                    publisher=publisher
                )
                sections_latex.append(section_latex)
        
        # Combine sections
        content_block = "\n".join(sections_latex)
        
        # Generate bibliography
        if publisher.lower() in ["acm"]:
            # BibTeX reference
            bibliography_block = "\\bibliographystyle{ACM-Reference-Format}\n\\bibliography{references}"
        else:
            # Inline bibliography
            bibliography_block = citation_engine.generate_latex_bibliography(publisher)
        
        # Replace placeholders in template
        final_latex = template.replace("{CONTENT}", content_block)
        final_latex = final_latex.replace("{BIBLIOGRAPHY}", bibliography_block)
        
        return final_latex
    
    def _extract_keywords_from_content(self, topic: str, abstract: str) -> List[str]:
        """Extract relevant keywords from topic and abstract using frequency analysis"""
        import re
        from collections import Counter

        text = f"{topic}. {abstract}".lower()

        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are', 'was',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'shall', 'can', 'need',
            'its', 'it', 'we', 'our', 'they', 'their', 'from', 'as', 'also', 'such',
            'which', 'where', 'when', 'how', 'what', 'who', 'more', 'most', 'very',
            'each', 'every', 'all', 'both', 'few', 'many', 'several', 'some', 'any',
            'not', 'no', 'nor', 'than', 'too', 'so', 'only', 'just', 'about', 'into',
            'over', 'after', 'before', 'between', 'under', 'through', 'during', 'while',
            'using', 'based', 'proposed', 'paper', 'approach', 'method', 'results',
            'show', 'shows', 'used', 'use', 'however', 'well', 'new', 'novel',
        }

        # Extract bigrams from text
        words = re.findall(r'\b[a-z]{3,}\b', text)
        filtered = [w for w in words if w not in stop_words]

        bigrams = [f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered) - 1)]
        bigram_counts = Counter(bigrams)

        # Extract single words
        word_counts = Counter(filtered)

        # Score bigrams higher, collect top candidates
        keywords = []
        for bg, cnt in bigram_counts.most_common(10):
            if cnt >= 1 and bg not in keywords:
                keywords.append(bg)
            if len(keywords) >= 3:
                break

        # Fill remaining with top single words not already covered by bigrams
        for w, cnt in word_counts.most_common(20):
            if len(keywords) >= 5:
                break
            if not any(w in kw for kw in keywords):
                keywords.append(w)

        # Ensure we have at least some keywords from the topic itself
        if not keywords:
            keywords = [w for w in topic.lower().split() if w not in stop_words and len(w) > 2][:5]

        return keywords[:5]
    
    def _save_latex_file(self, latex_content: str, topic: str, publisher: str) -> str:
        """Save LaTeX content to file"""
        # Create safe filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')
        
        filename = f"{safe_topic}_{publisher}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        logger.info(f"LaTeX file saved: {filepath}")
        return filepath
    
    def _save_bibliography(self, bibliography: str, topic: str) -> str:
        """Save BibTeX bibliography to file"""
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')
        
        filename = f"{safe_topic}_references_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(bibliography)
        
        logger.info(f"Bibliography file saved: {filepath}")
        return filepath
    
    def _compile_pdf(self, tex_filepath: str) -> Optional[str]:
        """Compile LaTeX file to PDF"""
        try:
            # Check if pdflatex is available
            subprocess.run([PDFLATEX_PATH, '--version'], 
                         capture_output=True, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("pdflatex not found. Install LaTeX to enable PDF generation.")
            logger.info("Windows: Download MiKTeX from https://miktex.org/")
            return None
        
        try:
            # Get directory and filename
            tex_dir = os.path.dirname(tex_filepath)
            tex_filename = os.path.basename(tex_filepath)
            pdf_filename = tex_filename.replace('.tex', '.pdf')
            pdf_filepath = os.path.join(tex_dir, pdf_filename)
            
            # Run pdflatex twice for proper references
            for i in range(2):
                result = subprocess.run(
                    [PDFLATEX_PATH, '-interaction=nonstopmode', '-output-directory', tex_dir, tex_filepath],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    logger.warning(f"pdflatex run {i+1} had warnings")
            
            # Check if PDF was created
            if os.path.exists(pdf_filepath):
                logger.info(f"PDF compiled successfully: {pdf_filepath}")
                
                # Clean up auxiliary files
                aux_extensions = ['.aux', '.log', '.out', '.bbl', '.blg']
                base_name = tex_filepath.replace('.tex', '')
                for ext in aux_extensions:
                    aux_file = base_name + ext
                    if os.path.exists(aux_file):
                        try:
                            os.remove(aux_file)
                        except:
                            pass
                
                return pdf_filepath
            else:
                logger.error("PDF file was not created")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("PDF compilation timed out")
            return None
        except Exception as e:
            logger.error(f"PDF compilation failed: {e}")
            return None
    
    def get_supported_publishers(self) -> List[str]:
        """Get list of supported publishers"""
        return list(SUPPORTED_PUBLISHERS.keys())
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all system components"""
        try:
            rag_stats = self.rag_engine.get_collection_stats()
            ai_info = self.ai_generator.get_model_info()
            
            return {
                "arxiv_fetcher": "Ready",
                "rag_engine": {
                    "status": rag_stats.get("status", "unknown"),
                    "total_papers": rag_stats.get("total_papers", 0),
                    "embedding_model": rag_stats.get("embedding_model", "unknown"),
                    "device": rag_stats.get("device", "unknown")
                },
                "ai_generator": {
                    "model_name": ai_info.get("model_name", "unknown"),
                    "device": ai_info.get("device", "unknown"),
                    "status": "ready"
                },
                "supported_publishers": self.get_supported_publishers(),
                "output_directory": OUTPUT_DIR
            }
        except Exception as e:
            return {
                "error": str(e),
                "arxiv_fetcher": "unknown",
                "rag_engine": {"status": "error", "total_papers": 0},
                "ai_generator": {"status": "error"},
                "supported_publishers": [],
                "output_directory": OUTPUT_DIR
            }

# Test function
def test_paper_generator():
    """Test the complete paper generation pipeline"""
    generator = ResearchPaperGenerator()
    
    # Test with a simple topic
    result = generator.generate_paper(
        topic="machine learning",
        publisher="ieee",
        paper_type="research",
        max_references=10,
        author_name="Test Author",
        author_email="test@example.com"
    )
    
    if result.get("success"):
        print("Paper generation successful!")
        print(f"Title: {result['title']}")
        print(f"Sections: {result['sections_generated']}")
        print(f"References: {result['references_used']}")
        print(f"LaTeX file: {result['files']['latex_file']}")
    else:
        print(f"Paper generation failed: {result.get('error')}")
    
    # Print system status
    status = generator.get_system_status()
    print(f"\nSystem Status: {status}")

if __name__ == "__main__":
    test_paper_generator()