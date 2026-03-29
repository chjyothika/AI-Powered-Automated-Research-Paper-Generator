import subprocess
import sys
import os

def check_latex():
    """Check if LaTeX is available"""
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ LaTeX (pdflatex) is available")
            print(f"Version: {result.stdout.split()[0]} {result.stdout.split()[1]}")
            return True
        else:
            print("✗ LaTeX (pdflatex) not working properly")
            return False
    except FileNotFoundError:
        print("✗ LaTeX (pdflatex) not found")
        print("\nTo install LaTeX:")
        print("Windows: Download MiKTeX from https://miktex.org/")
        print("Or use: winget install MiKTeX.MiKTeX")
        return False
    except Exception as e:
        print(f"✗ Error checking LaTeX: {e}")
        return False

def test_pdf_generation():
    """Test PDF generation with a simple LaTeX file"""
    if not check_latex():
        return False
    
    print("\nTesting PDF generation...")
    
    # Create simple test LaTeX file
    test_tex = """\\documentclass{article}
\\begin{document}
\\title{Test Document}
\\author{Test Author}
\\maketitle
\\section{Introduction}
This is a test document to verify PDF compilation works.
\\end{document}"""
    
    # Save test file
    os.makedirs("output", exist_ok=True)
    test_file = "output/test.tex"
    
    with open(test_file, 'w') as f:
        f.write(test_tex)
    
    # Try to compile
    try:
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', 
                               '-output-directory', 'output', test_file],
                              capture_output=True, text=True, timeout=30)
        
        pdf_file = "output/test.pdf"
        if os.path.exists(pdf_file):
            print("✓ PDF compilation successful!")
            print(f"Test PDF created: {pdf_file}")
            
            # Clean up
            for ext in ['.aux', '.log']:
                aux_file = f"output/test{ext}"
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            return True
        else:
            print("✗ PDF compilation failed")
            print(f"Error: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"✗ PDF compilation error: {e}")
        return False

if __name__ == "__main__":
    print("LaTeX PDF Compilation Test")
    print("=" * 30)
    
    if test_pdf_generation():
        print("\n🎉 PDF generation is ready!")
        print("The system can now generate PDF files automatically.")
    else:
        print("\n⚠️ PDF generation not available")
        print("LaTeX files will still be generated, but no PDF compilation.")
        print("Install LaTeX to enable PDF generation.")