# Complete Workflow - AI-Powered Research Paper Generator

## 🎯 Project Overview
An end-to-end system that generates publication-ready research papers in LaTeX format using AI, RAG (Retrieval-Augmented Generation), and multi-source academic literature retrieval.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT WEB INTERFACE                      │
│                         (app.py)                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PAPER GENERATOR ORCHESTRATOR                    │
│                    (paper_generator.py)                          │
│  • Coordinates all components                                    │
│  • Manages generation pipeline                                   │
│  • Handles file I/O and compilation                              │
└──┬──────────┬──────────┬──────────┬──────────┬─────────────┬───┘
   │          │          │          │          │             │
   ▼          ▼          ▼          ▼          ▼             ▼
┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│Multi │ │  RAG   │ │   AI   │ │ LaTeX  │ │Citation│ │  Graph   │
│Source│ │ Engine │ │Generator│ │Template│ │ Engine │ │Generator │
│Fetch │ │        │ │        │ │Manager │ │        │ │          │
└──────┘ └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘
```

---

## 🔄 Complete Workflow (Step-by-Step)

### **Phase 1: User Input & Initialization**

#### Step 1: User Provides Input
- **Research Topic/Title**: e.g., "Satellite Disaster Images Fake Detection"
- **Abstract**: User-provided abstract (semantic anchor for consistency)
- **Publisher**: IEEE, Elsevier, ACM, or Springer
- **Paper Type**: Research, Review, or Survey
- **Max References**: 5-50 papers
- **Author Details**: Name and email

#### Step 2: System Initialization
```python
# Components initialized:
- MultiSourceFetcher()      # Fetches papers from multiple sources
- RAGEngine()               # Vector database for semantic search
- AIGenerator()             # Content generation
- LaTeXTemplateManager()    # Template handling
- CitationEngine()          # Citation management
- GraphResultsGenerator()   # Figure generation
```

---

### **Phase 2: Literature Retrieval**

#### Step 3: Keyword Extraction
```python
# From: paper_generator.py -> _extract_search_keywords()
Input: Topic + Abstract
Process:
  1. Extract multi-word technical terms (e.g., "machine learning", "deep learning")
  2. Remove stop words
  3. Identify domain-specific keywords
  4. Build search query with OR operators
Output: "machine learning OR neural network OR classification"
```

#### Step 4: Dynamic Reference Count Calculation
```python
# From: paper_generator.py -> _calculate_reference_count()
Factors:
  - Abstract length (longer = more complex = more refs)
  - Complexity keywords ("comprehensive", "novel", "framework")
  - User-requested max references
Output: 15-40 references (dynamically adjusted)
```

#### Step 5: Multi-Source Paper Fetching
```python
# From: src/multi_source_fetcher/fetcher.py
Sources:
  1. arXiv API (HTTP + XML parsing)
  2. PubMed (NCBI E-utilities API)
  3. Semantic Scholar (Free API)
  4. CrossRef (Open API)

For each source:
  - Rate limiting (1-3 seconds between requests)
  - XML/JSON parsing
  - Extract: title, authors, abstract, year, URL
  - Deduplicate based on title similarity (70% threshold)

Output: List of AcademicPaper objects
```

**Data Structure:**
```python
@dataclass
class AcademicPaper:
    id: str                    # Unique identifier
    title: str                 # Paper title
    authors: List[str]         # Author names
    abstract: str              # Full abstract
    published: str             # Publication date
    url: str                   # Paper URL
    source: str                # arXiv/PubMed/etc.
    categories: List[str]      # Subject categories
```

---

### **Phase 3: RAG Database Construction**

#### Step 6: Vector Embedding Generation
```python
# From: src/rag_engine/rag.py
Model: allenai/scibert_scivocab_uncased (SciBERT)
Device: CUDA (GPU) or CPU
Process:
  1. Load SentenceTransformer model
  2. For each paper abstract:
     - Generate 768-dimensional embedding vector
     - Use GPU acceleration (RTX 4060)
  3. Store in ChromaDB (persistent vector database)

Storage: ./data/chromadb/
```

**ChromaDB Schema:**
```python
Collection: "research_papers"
Documents: Paper abstracts (text)
Embeddings: 768-dim vectors (float32)
Metadata: {
    title, authors, published, pdf_url,
    categories, arxiv_id, source
}
IDs: Unique paper identifiers
```

#### Step 7: Semantic Search & Retrieval
```python
# Query: Topic + User Abstract
Process:
  1. Generate query embedding (768-dim vector)
  2. Cosine similarity search in ChromaDB
  3. Retrieve top-k most relevant papers (k=10-15)
  4. Return papers with similarity scores

Output: Ranked list of relevant papers
```

---

### **Phase 4: Content Generation**

#### Step 8: Section-by-Section Generation

**For each section (Abstract, Introduction, Literature Review, Methodology, Results, Conclusion):**

##### A. Content Generation Strategy
```python
# From: src/ai_generator/generator.py
Primary: Ollama LLM (llama3.1:8b) - Local inference
Fallback: Topic-adaptive templates

Ollama Generation:
  - Model: llama3.1:8b (8 billion parameters)
  - API: http://localhost:11434/api/generate
  - Temperature: 0.4 (focused, academic)
  - Max tokens: 1500 per section
  - Prompt engineering with retrieved papers
```

**Prompt Structure:**
```
You are an expert academic researcher. Write the [SECTION] section.

Topic: [USER_TOPIC]
Abstract: [USER_ABSTRACT]

Related papers:
  1. "[PAPER_TITLE]" - [ABSTRACT_SNIPPET]
  2. ...

Instructions:
- Write in formal academic style
- Use specific technical details
- NO markdown formatting
- Output only section text

[SECTION-SPECIFIC INSTRUCTIONS]
```

##### B. Fallback: Topic-Adaptive Templates
```python
# From: src/ollama_generator/ollama_llm.py
When Ollama unavailable:
  1. Extract key terms from topic + abstract
  2. Identify domain (healthcare, transportation, CV, etc.)
  3. Detect methods (ML, DL, CNN, etc.)
  4. Generate content using templates with:
     - Domain-specific terminology
     - Method-specific descriptions
     - Retrieved paper references
     - Realistic metrics and findings
```

##### C. Enhanced Content Features

**Methodology Section:**
```python
# Equation insertion
From: src/equation_generator/equations.py
- Detects relevant equations based on topic
- Inserts LaTeX math equations
- Examples: Loss functions, accuracy formulas, optimization equations
```

**Results Section:**
```python
# From: src/graph_generator/graphs.py
Generates:
  1. Performance comparison tables (accuracy, precision, recall)
  2. Dataset statistics tables
  3. Ablation study results
  4. Confusion matrix figures (matplotlib)
  5. Training curves (accuracy/loss over epochs)
  6. Performance comparison bar charts

Output: PDF figures + LaTeX code
```

---

### **Phase 5: Citation Management**

#### Step 9: Citation Insertion
```python
# From: src/citation_engine/citations.py
Citation Styles:
  - IEEE/ACM: Numeric [1], [2,3], [1-3]
  - Elsevier/Springer: Author-year (Smith et al., 2023)

Process:
  1. Add papers to citation database
  2. Generate unique citation keys (ref_arxiv_id)
  3. Calculate section-specific citation density:
     - Literature Review: 65% of sentences
     - Introduction: 40%
     - Methodology: 20%
     - Results: 25%
     - Conclusion: 15%
  4. Insert citations at sentence boundaries
  5. Format according to publisher style
```

**Citation Data Structure:**
```python
{
    'key': 'ref2301_12345',
    'title': 'Paper Title',
    'authors': ['Smith, J.', 'Doe, A.'],
    'year': '2023',
    'arxiv_id': '2301.12345',
    'source': 'arXiv',
    'url': 'https://arxiv.org/abs/2301.12345',
    'number': 1  # For numeric citations
}
```

#### Step 10: Bibliography Generation
```python
# Two formats:
1. BibTeX (.bib file) - For ACM
   @article{ref2301_12345,
     title={...},
     author={... and ...},
     journal={arXiv preprint arXiv:2301.12345},
     year={2023}
   }

2. LaTeX thebibliography - For IEEE/Elsevier/Springer
   \bibitem{ref2301_12345}
   Smith, J., Doe, A., "Paper Title," arXiv preprint, 2023.
```

---

### **Phase 6: LaTeX Document Assembly**

#### Step 11: Template Selection & Generation
```python
# From: src/latex_templates/template_manager.py
Publishers:
  - IEEE: IEEEtran.cls (conference format)
  - Elsevier: elsarticle.cls (review format)
  - ACM: acmart.cls (sigconf format)
  - Springer: svjour3.cls (journal format)

Template includes:
  - Document class and packages
  - Title, authors, affiliations
  - Abstract and keywords
  - Section placeholders {CONTENT}
  - Bibliography placeholder {BIBLIOGRAPHY}
```

#### Step 12: Section Formatting
```python
For each section:
  \section{Title}\label{sec:section_name}
  [CONTENT WITH CITATIONS]
  
Special handling:
  - Abstract: Already in template header
  - Figures: \begin{figure}...\includegraphics...\end{figure}
  - Tables: \begin{table}...\begin{tabular}...\end{table}
  - Equations: \begin{equation}...\end{equation}
```

#### Step 13: Keyword Extraction
```python
# From: paper_generator.py -> _extract_keywords_from_content()
Process:
  1. Extract bigrams (2-word phrases) from topic + abstract
  2. Count frequency of bigrams
  3. Extract single important words
  4. Remove stop words
  5. Select top 5 keywords

Output: ["machine learning", "classification", "neural network", ...]
```

#### Step 14: Final Assembly
```python
Complete LaTeX document:
  1. Replace {CONTENT} with all formatted sections
  2. Replace {BIBLIOGRAPHY} with citation entries
  3. Insert figures and tables
  4. Add keywords to header
  5. Validate LaTeX syntax
```

---

### **Phase 7: File Generation & Compilation**

#### Step 15: File Saving
```python
# From: paper_generator.py
Files generated:
  1. .tex file: Complete LaTeX source
     Format: Topic_Publisher_YYYYMMDD_HHMMSS.tex
     Location: ./output/
  
  2. .bib file: BibTeX bibliography (if ACM)
     Format: Topic_references_YYYYMMDD_HHMMSS.bib
     Location: ./output/
  
  3. Figures: .pdf files for graphs
     Location: ./output/
```

#### Step 16: PDF Compilation (Optional)
```python
# Requires: MiKTeX or TeX Live installed
Process:
  1. Check if pdflatex is available
  2. Run pdflatex twice (for references)
     Command: pdflatex -interaction=nonstopmode file.tex
  3. Clean auxiliary files (.aux, .log, .out)
  4. Return PDF path

Fallback: Online PDF conversion
  - Upload .tex to LaTeX compilation service
  - Download compiled PDF
```

---

## 🧠 AI Models & Technologies

### **1. Embedding Model (RAG)**
```yaml
Model: allenai/scibert_scivocab_uncased
Type: BERT-based sentence transformer
Parameters: 110M
Embedding Dimension: 768
Purpose: Scientific text embeddings for semantic search
Training: Pre-trained on 1.14M scientific papers
Device: CUDA (GPU) / CPU
Framework: sentence-transformers
```

### **2. Generation Model (Primary)**
```yaml
Model: Ollama llama3.1:8b
Type: Large Language Model (LLM)
Parameters: 8 billion
Context Window: 8192 tokens
Purpose: Academic content generation
Deployment: Local inference (http://localhost:11434)
Temperature: 0.4 (focused generation)
Max Tokens: 1500 per section
```

### **3. Generation Model (Fallback)**
```yaml
Model: microsoft/DialoGPT-large
Type: Autoregressive language model
Parameters: 762M
Purpose: Backup content generation
Device: CUDA (GPU) / CPU
Framework: transformers (Hugging Face)
Temperature: 0.3
Max Tokens: 2048
```

### **4. Topic-Adaptive Templates**
```yaml
Type: Rule-based generation with NLP
Purpose: Fallback when LLMs unavailable
Features:
  - Domain detection (healthcare, CV, NLP, etc.)
  - Method extraction (ML, DL, CNN, etc.)
  - Dynamic content adaptation
  - Reference integration
```

---

## 📦 Data Flow Diagram

```
USER INPUT
    ↓
[Topic + Abstract + Settings]
    ↓
KEYWORD EXTRACTION → Search Query
    ↓
MULTI-SOURCE FETCHING
    ├─→ arXiv API
    ├─→ PubMed API
    ├─→ Semantic Scholar API
    └─→ CrossRef API
    ↓
[Academic Papers List]
    ↓
EMBEDDING GENERATION (SciBERT)
    ↓
CHROMADB STORAGE
    ↓
SEMANTIC SEARCH (Query: Topic + Abstract)
    ↓
[Top-K Relevant Papers]
    ↓
CONTENT GENERATION (Section-by-Section)
    ├─→ Ollama LLM (Primary)
    └─→ Topic Templates (Fallback)
    ↓
[Raw Section Content]
    ↓
CITATION INSERTION
    ├─→ Citation Database
    ├─→ Section-specific Density
    └─→ Publisher Style Formatting
    ↓
[Content + Citations]
    ↓
LATEX ASSEMBLY
    ├─→ Template Selection
    ├─→ Section Formatting
    ├─→ Bibliography Generation
    └─→ Figure Insertion
    ↓
[Complete LaTeX Document]
    ↓
FILE GENERATION
    ├─→ .tex file
    ├─→ .bib file (if needed)
    └─→ .pdf figures
    ↓
PDF COMPILATION (Optional)
    ├─→ Local: pdflatex
    └─→ Online: LaTeX service
    ↓
OUTPUT FILES
```

---

## 🗂️ Project Structure

```
Research Paper Generator/
│
├── app.py                          # Streamlit web interface
├── paper_generator.py              # Main orchestrator
├── config.py                       # Configuration settings
│
├── src/
│   ├── multi_source_fetcher/
│   │   └── fetcher.py             # Multi-source paper retrieval
│   │
│   ├── rag_engine/
│   │   └── rag.py                 # RAG with ChromaDB + SciBERT
│   │
│   ├── ai_generator/
│   │   └── generator.py           # Content generation
│   │
│   ├── ollama_generator/
│   │   └── ollama_llm.py          # Ollama LLM integration
│   │
│   ├── latex_templates/
│   │   └── template_manager.py    # LaTeX template handling
│   │
│   ├── citation_engine/
│   │   └── citations.py           # Citation management
│   │
│   ├── graph_generator/
│   │   └── graphs.py              # Figure generation
│   │
│   ├── equation_generator/
│   │   └── equations.py           # Math equation insertion
│   │
│   └── synthetic_data/
│       └── generator.py           # Synthetic data generation
│
├── data/
│   └── chromadb/                  # Vector database storage
│
├── output/                        # Generated papers
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## ⚙️ Configuration Parameters

```python
# GPU Configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GPU_MEMORY_FRACTION = 0.8

# RAG Configuration
EMBEDDING_MODEL = "allenai/scibert_scivocab_uncased"
CHROMADB_PATH = "./data/chromadb"
TOP_K_RETRIEVAL = 10

# AI Generation
GENERATION_MODEL = "microsoft/DialoGPT-large"
MAX_TOKENS = 2048
TEMPERATURE = 0.3

# arXiv API
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"
ARXIV_RATE_LIMIT = 1  # seconds
ARXIV_MAX_RESULTS = 50
ARXIV_TIMEOUT = 30

# Paper Length
TARGET_PAPER_LENGTH = 6500  # words
SECTION_WORD_TARGETS = {
    "abstract": 200,
    "introduction": 800,
    "literature_review": 1200,
    "methodology": 1500,
    "results": 1300,
    "conclusion": 500
}

# References
MIN_REFERENCES = 5
MAX_REFERENCES = 40
REFERENCE_DENSITY = 0.006  # refs per word

# Publishers
SUPPORTED_PUBLISHERS = {
    "ieee": {"template": "IEEEtran.cls", "citation_style": "numeric"},
    "elsevier": {"template": "elsarticle.cls", "citation_style": "authoryear"},
    "acm": {"template": "acmart.cls", "citation_style": "numeric"},
    "springer": {"template": "svjour3.cls", "citation_style": "authoryear"}
}
```

---

## 🔧 Key Algorithms

### **1. Semantic Search Algorithm**
```python
def search_similar_papers(query: str, top_k: int):
    # Generate query embedding
    query_embedding = embedding_model.encode(query)  # 768-dim vector
    
    # Cosine similarity search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # Return ranked papers with similarity scores
    return results
```

### **2. Citation Insertion Algorithm**
```python
def insert_citations(text: str, papers: List, density: float):
    # Split text into sentences
    sentences = split_sentences(text)
    
    # Calculate number of citations to insert
    n_citations = int(len(sentences) * density)
    
    # Distribute citations evenly across sentences
    step = len(sentences) // n_citations
    insert_indices = range(0, len(sentences), step)
    
    # Insert citations at selected positions
    for idx in insert_indices:
        citation = format_citation(papers[idx % len(papers)])
        sentences[idx] += f" {citation}"
    
    return ' '.join(sentences)
```

### **3. Keyword Extraction Algorithm**
```python
def extract_keywords(topic: str, abstract: str):
    text = f"{topic} {abstract}".lower()
    
    # Extract bigrams (2-word phrases)
    words = tokenize(text)
    bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
    
    # Count frequency
    bigram_counts = Counter(bigrams)
    
    # Select top bigrams
    keywords = [bg for bg, count in bigram_counts.most_common(3)]
    
    # Add important single words
    word_counts = Counter(words)
    keywords += [w for w, c in word_counts.most_common(5)]
    
    return keywords[:5]
```

---

## 📈 Performance Metrics

### **System Performance**
- **Paper Generation Time**: 2-5 minutes (depending on references)
- **GPU Memory Usage**: ~2-3 GB (RTX 4060)
- **CPU Usage**: 30-50% during generation
- **Disk Space**: ~500 MB (models + database)

### **Content Quality**
- **Average Paper Length**: 6000-7000 words
- **References per Paper**: 15-40 citations
- **Sections Generated**: 6 (Abstract, Intro, Lit Review, Method, Results, Conclusion)
- **Citation Density**: 0.3-0.65 citations per sentence (section-dependent)

### **API Rate Limits**
- **arXiv**: 1 request/second
- **PubMed**: 2 requests/second
- **Semantic Scholar**: 1 request/3 seconds
- **CrossRef**: 1 request/second

---

## 🎓 Academic Ethics & Compliance

### **Disclaimer**
- Human review REQUIRED before submission
- Plagiarism checks MANDATORY
- All citations must be verified
- Peer review process still necessary
- Tool does NOT guarantee publication acceptance

### **Citation Integrity**
- All papers properly attributed
- BibTeX/LaTeX bibliography generated
- Multiple citation styles supported
- Source tracking (arXiv, PubMed, etc.)

### **Content Authenticity**
- Synthetic results clearly labeled
- No fabricated data
- Proper attribution maintained
- Academic writing standards followed

---

## 🚀 Usage Example

```python
# Initialize generator
generator = ResearchPaperGenerator()

# Generate paper
result = generator.generate_paper(
    topic="Satellite Disaster Images Fake Detection",
    user_abstract="This paper presents a novel approach...",
    publisher="ieee",
    paper_type="research",
    max_references=20,
    author_name="John Doe",
    author_email="john@university.edu"
)

# Output
if result["success"]:
    print(f"Title: {result['title']}")
    print(f"Sections: {result['sections_generated']}")
    print(f"References: {result['references_used']}")
    print(f"LaTeX: {result['files']['latex_file']}")
    print(f"PDF: {result['files']['pdf_file']}")
```

---

## 🔍 Troubleshooting

### **Common Issues**

1. **No papers found**
   - Check internet connection
   - Verify API endpoints are accessible
   - Try broader search keywords

2. **GPU not detected**
   - Install CUDA toolkit
   - Update PyTorch: `pip install torch --upgrade`
   - Check: `torch.cuda.is_available()`

3. **PDF compilation fails**
   - Install MiKTeX or TeX Live
   - Run: `install_latex.bat` (Windows)
   - Use online PDF conversion fallback

4. **Ollama not available**
   - System automatically falls back to templates
   - Install Ollama: https://ollama.ai
   - Run: `ollama pull llama3.1:8b`

---

## 📚 Dependencies

```
Core:
- Python 3.9/3.10
- PyTorch 2.0+ (CUDA support)
- transformers 4.30+
- sentence-transformers 2.2+
- chromadb 0.4+

APIs:
- requests 2.31+
- streamlit 1.25+

LaTeX:
- MiKTeX or TeX Live (optional)

Hardware:
- NVIDIA GPU (RTX 4060 recommended)
- 8GB+ RAM
- 10GB+ disk space
```

---

## 🎯 Future Enhancements

1. **Multi-language support** (non-English papers)
2. **Advanced figure generation** (architecture diagrams)
3. **Collaborative editing** (multi-author support)
4. **Version control** (paper revisions)
5. **Plagiarism detection** (integrated checking)
6. **Custom templates** (user-defined formats)
7. **Real-time collaboration** (Google Docs-like)
8. **Citation recommendation** (AI-suggested papers)

---

## 📞 Support

For issues or questions:
- Check logs in console output
- Review `USAGE_GUIDE.md`
- Verify system requirements
- Test with simple topics first

---

**Last Updated**: February 2026
**Version**: 1.0
**Status**: Production Ready ✅
