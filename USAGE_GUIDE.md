# AI-Powered Research Paper Generator - Usage Guide

## 🚀 Quick Start

### 1. Installation
```bash
# Run the setup script
python setup.py
```

### 2. Start the Web Interface
```bash
streamlit run app.py
```

### 3. Generate Your First Paper
1. Enter a research topic (e.g., "machine learning")
2. Select target publisher (IEEE, Elsevier, ACM, Springer)
3. Choose paper type (Research, Review, Survey)
4. Click "Generate Research Paper"
5. Download the generated LaTeX and bibliography files

## 📋 Detailed Usage

### Web Interface (Recommended)
The Streamlit web interface provides the easiest way to use the system:

- **User-friendly forms** for all inputs
- **Real-time progress** tracking
- **Instant preview** of generated content
- **One-click downloads** for LaTeX files
- **System status** monitoring

### Command Line Interface
For programmatic use or automation:

```python
from paper_generator import ResearchPaperGenerator

generator = ResearchPaperGenerator()

result = generator.generate_paper(
    topic="neural networks",
    publisher="ieee",
    paper_type="research",
    max_references=20,
    author_name="Your Name",
    author_email="your.email@institution.edu"
)

if result["success"]:
    print(f"Paper generated: {result['files']['latex_file']}")
else:
    print(f"Generation failed: {result['error']}")
```

## 🎯 Best Practices

### Topic Selection
- **Be specific**: "convolutional neural networks for image classification" vs "AI"
- **Use academic terms**: Technical terminology yields better results
- **Check arXiv availability**: Ensure papers exist on your topic

### Publisher Selection
- **IEEE**: Numeric citations [1], conference/journal format
- **Elsevier**: Author-year citations (Smith et al., 2023)
- **ACM**: Numeric citations, specific formatting
- **Springer**: Author-year citations, journal format

### Paper Types
- **Research**: Novel methods, experiments, results
- **Review**: Comprehensive analysis of existing work
- **Survey**: Broad overview of a field

## 📁 Output Files

### LaTeX File (.tex)
- Complete paper with all sections
- Publisher-specific formatting
- Embedded citations
- Ready for compilation

### Bibliography File (.bib) - When Applicable
- BibTeX format for ACM papers
- All referenced papers
- Proper academic formatting

## 🔧 Configuration

### GPU Settings
Edit `config.py` to adjust GPU usage:
```python
DEVICE = "cuda"  # or "cpu"
GPU_MEMORY_FRACTION = 0.8
```

### Model Settings
```python
GENERATION_MODEL = "microsoft/DialoGPT-medium"
MAX_TOKENS = 512
TEMPERATURE = 0.7
```

### arXiv Settings
```python
ARXIV_MAX_RESULTS = 50
ARXIV_RATE_LIMIT = 3  # seconds between requests
```

## 🧪 Testing

### Run All Tests
```bash
python test_system.py
```

### Test Individual Components
```python
# Test arXiv fetcher
from src.arxiv_fetcher import ArxivFetcher
fetcher = ArxivFetcher()
papers = fetcher.search_papers("machine learning", max_results=5)

# Test RAG engine
from src.rag_engine import RAGEngine
rag = RAGEngine()
rag.add_papers(papers)

# Test AI generator
from src.ai_generator import AIGenerator
generator = AIGenerator()
content = generator.generate_section("introduction", "machine learning")
```

## 📊 System Monitoring

### Check System Status
```python
from paper_generator import ResearchPaperGenerator
generator = ResearchPaperGenerator()
status = generator.get_system_status()
print(status)
```

### Monitor RAG Database
```python
from src.rag_engine import RAGEngine
rag = RAGEngine()
stats = rag.get_collection_stats()
print(f"Papers in database: {stats['total_papers']}")
```

## 🚨 Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory
```python
# In config.py, reduce GPU memory usage
GPU_MEMORY_FRACTION = 0.5

# Or use CPU only
DEVICE = "cpu"
```

#### 2. arXiv Rate Limiting
```python
# Increase rate limit delay
ARXIV_RATE_LIMIT = 5  # seconds
```

#### 3. Model Download Failures
```bash
# Set proxy if needed
export HF_HUB_PROXY=http://your-proxy:port

# Or download manually
python -c "from transformers import AutoModel; AutoModel.from_pretrained('microsoft/DialoGPT-medium')"
```

#### 4. ChromaDB Issues
```bash
# Clear database if corrupted
rm -rf data/chromadb
```

### Error Messages

#### "No papers found on arXiv"
- Try broader search terms
- Check internet connection
- Verify topic has academic papers

#### "Model loading failed"
- Check GPU memory
- Try CPU mode
- Verify model downloads

#### "Template generation failed"
- Check publisher name spelling
- Verify supported publishers list

## 📈 Performance Optimization

### For Speed
- Use smaller models
- Reduce `MAX_TOKENS`
- Limit `max_references`
- Use CPU for small tasks

### For Quality
- Increase `MAX_TOKENS`
- Use more references
- Lower `TEMPERATURE` for consistency
- Use GPU acceleration

## 🔒 Academic Ethics

### IMPORTANT DISCLAIMERS
- **Human review required** before any submission
- **Plagiarism checks mandatory**
- **Citation verification essential**
- **Peer review still necessary**

### Ethical Usage
1. Use as a **starting point**, not final product
2. **Verify all claims** and citations
3. **Add original contributions**
4. **Follow institutional guidelines**
5. **Respect copyright** and fair use

### What This Tool Does
✅ Assists with paper structure
✅ Provides literature review starting points
✅ Generates proper LaTeX formatting
✅ Creates citation frameworks

### What This Tool Does NOT Do
❌ Replace human expertise
❌ Guarantee publication
❌ Ensure originality
❌ Validate scientific claims

## 📚 Advanced Usage

### Custom Models
```python
# Use different generation model
from src.ai_generator import AIGenerator
generator = AIGenerator("gpt2-large")
```

### Batch Processing
```python
topics = ["neural networks", "computer vision", "NLP"]
for topic in topics:
    result = generator.generate_paper(topic=topic)
    print(f"Generated paper for {topic}")
```

### Custom Templates
Add new publisher templates in `src/latex_templates/template_manager.py`:
```python
def _get_custom_template(self, title, authors, abstract):
    return """\\documentclass{custom}
    % Your custom template here
    """
```

## 🆘 Getting Help

### Check Logs
```bash
# View detailed logs
tail -f logs/paper_generator.log
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Community Support
- Check GitHub issues
- Review documentation
- Test with minimal examples

## 📋 Checklist for Paper Submission

Before submitting any generated paper:

- [ ] Human review completed
- [ ] Plagiarism check performed
- [ ] All citations verified
- [ ] Original contributions added
- [ ] Methodology validated
- [ ] Results verified
- [ ] Institutional approval obtained
- [ ] Publisher guidelines followed
- [ ] Ethical considerations addressed
- [ ] Peer review completed

Remember: This tool assists with paper preparation but cannot replace human expertise, original research, or proper academic processes.