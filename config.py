"""
Configuration settings for the Research Paper Generator
"""
import torch

# GPU Configuration
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Device: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    DEVICE = "cuda"
else:
    print("CUDA not available - using CPU")
    DEVICE = "cpu"
print(f"Device set to use: {DEVICE}")
GPU_MEMORY_FRACTION = 0.8  # Use 80% of GPU memory

# RAG Configuration - Use SciBERT for scientific embeddings
EMBEDDING_MODEL = "allenai/scibert_scivocab_uncased"  # SciBERT for scientific text
CHROMADB_PATH = "./data/chromadb"
TOP_K_RETRIEVAL = 10

# AI Generation Configuration - Better model for academic writing
GENERATION_MODEL = "microsoft/DialoGPT-large"  # Larger model for better quality
MAX_TOKENS = 2048  # Increased for longer content
TEMPERATURE = 0.3  # Lower temperature for more focused academic writing

# arXiv API Configuration
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"
ARXIV_USER_AGENT = "ResearchPaperGenerator/1.0 (Academic Research Tool)"
ARXIV_RATE_LIMIT = 1  # Reduced for better reliability
ARXIV_MAX_RESULTS = 50
ARXIV_TIMEOUT = 30  # Increased timeout

# Long Paper Configuration (7-8 pages)
TARGET_PAPER_LENGTH = 6500  # Target word count
SECTION_WORD_TARGETS = {
    "abstract": 200,
    "introduction": 800,
    "literature_review": 1200,
    "methodology": 1500,
    "results": 1300,
    "conclusion": 500
}

# Reference Scaling
MIN_REFERENCES = 5
MAX_REFERENCES = 40
REFERENCE_DENSITY = 0.006  # References per word

# LaTeX Templates
SUPPORTED_PUBLISHERS = {
    "ieee": {
        "template": "IEEEtran.cls",
        "citation_style": "numeric",
        "url": "https://www.ieee.org/conferences/publishing/templates.html"
    },
    "elsevier": {
        "template": "elsarticle.cls", 
        "citation_style": "authoryear",
        "url": "https://www.elsevier.com/authors/policies-and-guidelines/latex-instructions"
    },
    "acm": {
        "template": "acmart.cls",
        "citation_style": "numeric", 
        "url": "https://www.acm.org/publications/proceedings-template"
    },
    "springer": {
        "template": "svjour3.cls",
        "citation_style": "authoryear",
        "url": "https://www.springer.com/gp/authors-editors/book-authors-editors/manuscript-preparation/5636"
    }
}

# Paper Structure
PAPER_SECTIONS = [
    "abstract",
    "introduction", 
    "literature_review",
    "methodology",
    "results",
    "conclusion"
]

# Output Configuration
OUTPUT_DIR = "./output"
LATEX_COMPILE = False  # LaTeX not installed - set to True after installing LaTeX
PDFLATEX_PATH = "pdflatex"  # System pdflatex command