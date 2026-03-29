"""
Enable PDF generation after LaTeX installation
"""
import subprocess
import sys

def check_latex():
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def enable_pdf():
    if check_latex():
        # Update config.py to enable LaTeX compilation
        with open('config.py', 'r') as f:
            content = f.read()
        
        content = content.replace('LATEX_COMPILE = False', 'LATEX_COMPILE = True')
        
        with open('config.py', 'w') as f:
            f.write(content)
        
        print("✅ PDF generation enabled!")
        print("You can now generate PDF files along with LaTeX files.")
    else:
        print("❌ LaTeX not found. Please install MiKTeX first.")
        print("Run: install_latex.bat")

if __name__ == "__main__":
    enable_pdf()