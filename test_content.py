import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_generator import AIGenerator

# Test with road accident safety prediction
generator = AIGenerator()

print("Testing road accident safety prediction content generation...")
print("=" * 60)

# Test abstract generation
abstract = generator.generate_section("abstract", "road accident safety prediction")
print("ABSTRACT:")
print(abstract)
print("\n" + "=" * 60)

# Test introduction generation  
intro = generator.generate_section("introduction", "road accident safety prediction")
print("INTRODUCTION:")
print(intro[:500] + "..." if len(intro) > 500 else intro)
print(f"\nFull length: {len(intro)} characters")