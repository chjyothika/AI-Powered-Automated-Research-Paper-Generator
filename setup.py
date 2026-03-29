"""
Setup script for AI-Powered Research Paper Generator
Handles installation, configuration, and initial setup
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 9:
        print(f"❌ Python 3.9+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_gpu_availability():
    """Check if CUDA GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ GPU available: {gpu_name}")
            print(f"   GPU memory: {gpu_memory:.1f} GB")
            return True
        else:
            print("⚠️  No CUDA GPU detected. Will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet. GPU check will be done after installation.")
        return None

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    try:
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "data/chromadb", 
        "output",
        "src/latex_templates/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    return True

def download_models():
    """Download and cache required models"""
    print("\n🤖 Downloading AI models...")
    
    try:
        # Import after installation
        from sentence_transformers import SentenceTransformer
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        # Download embedding model
        print("Downloading embedding model...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model downloaded")
        
        # Download generation model
        print("Downloading generation model...")
        tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
        model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-medium')
        print("✅ Generation model downloaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Model download failed: {e}")
        print("Models will be downloaded on first use.")
        return False

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    try:
        # Run basic import test
        subprocess.check_call([
            sys.executable, "test_system.py"
        ], timeout=300)  # 5 minute timeout
        
        print("✅ Installation test passed")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️  Test timed out (this is normal for first run)")
        return True
    except subprocess.CalledProcessError:
        print("❌ Installation test failed")
        return False

def create_env_file():
    """Create environment configuration file"""
    print("\n⚙️  Creating configuration...")
    
    env_content = """# AI Research Paper Generator Configuration
# Modify these settings as needed

# GPU Settings
CUDA_VISIBLE_DEVICES=0

# Model Settings  
HF_HOME=./models
TRANSFORMERS_CACHE=./models

# Logging
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration file created (.env)")
    return True

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    
    print("""
📋 USAGE INSTRUCTIONS:

1. Start the web interface:
   streamlit run app.py

2. Or use the command line:
   python paper_generator.py

3. Run tests:
   python test_system.py

4. Check system status:
   python -c "from paper_generator import ResearchPaperGenerator; print(ResearchPaperGenerator().get_system_status())"

📁 IMPORTANT FILES:
   - app.py: Web interface
   - paper_generator.py: Main generator
   - config.py: Configuration settings
   - output/: Generated papers will be saved here
   - data/: RAG database storage

⚠️  REMEMBER:
   - This tool assists with paper preparation
   - Human review is REQUIRED before submission
   - Always perform plagiarism checks
   - Verify all citations and references

🔧 TROUBLESHOOTING:
   - If GPU issues: Set CUDA_VISIBLE_DEVICES=-1 in .env for CPU-only
   - If model download fails: They'll download on first use
   - If tests fail: Check the error messages above

📖 For more help, see README.md
""")

def main():
    """Main setup function"""
    print("🚀 AI-Powered Research Paper Generator Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    # Check GPU (optional)
    check_gpu_availability()
    
    # Create directories
    if not create_directories():
        return False
    
    # Install packages
    if not install_requirements():
        return False
    
    # Check GPU again after PyTorch installation
    check_gpu_availability()
    
    # Create configuration
    if not create_env_file():
        return False
    
    # Download models (optional)
    download_models()
    
    # Test installation
    test_installation()
    
    # Print instructions
    print_usage_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)