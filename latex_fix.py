#!/usr/bin/env python3
"""
LaTeX Fix Utility - Clean up LaTeX formatting issues
"""

import re

def fix_latex_content(content: str) -> str:
    """Fix common LaTeX formatting issues"""
    
    # Fix special characters
    content = content.replace('#', '\\#')
    content = content.replace('&', '\\&')
    content = content.replace('%', '\\%')
    content = content.replace('$', '\\$')
    
    # Fix malformed textbf commands
    content = re.sub(r'\\textbf\{([^}]*?)\\textbf\{', r'\\textbf{\1}', content)
    content = re.sub(r'\\textbf\{([^}]*?)$', r'\\textbf{\1}', content, flags=re.MULTILINE)
    
    # Fix equation newlines
    content = re.sub(r'\\begin\{equation\}\\n', r'\\begin{equation}\\\\', content)
    content = re.sub(r'\\n\\end\{equation\}', r'\\\\\\end{equation}', content)
    
    # Fix broken textbf
    content = re.sub(r'\\textbf\{([^}]+)\\textbf\{', r'\\textbf{\1}', content)
    
    return content

def fix_latex_file(filepath: str):
    """Fix LaTeX file in place"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_latex_content(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed LaTeX file: {filepath}")
        
    except Exception as e:
        print(f"Error fixing file {filepath}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        fix_latex_file(sys.argv[1])
    else:
        print("Usage: python latex_fix.py <file.tex>")