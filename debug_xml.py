import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import xml.etree.ElementTree as ET

# Get the XML response
base_url = "http://export.arxiv.org/api/query"
params = {
    "search_query": "all:neural networks",
    "start": 0,
    "max_results": 3
}
headers = {
    "User-Agent": "ScopusReadyPaperGenerator/1.0 (academic project)"
}

response = requests.get(base_url, params=params, headers=headers, timeout=20)
xml_content = response.text

print("XML Response:")
print(xml_content[:1000])
print("\n" + "="*50)

# Parse with our method
try:
    root = ET.fromstring(xml_content)
    
    # Define namespaces used by arXiv
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    entries = root.findall('atom:entry', namespaces)
    print(f"Found {len(entries)} entries")
    
    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}:")
        
        # Extract basic information
        id_elem = entry.find('atom:id', namespaces)
        title_elem = entry.find('atom:title', namespaces)
        summary_elem = entry.find('atom:summary', namespaces)
        published_elem = entry.find('atom:published', namespaces)
        
        print(f"ID found: {id_elem is not None}")
        print(f"Title found: {title_elem is not None}")
        print(f"Summary found: {summary_elem is not None}")
        print(f"Published found: {published_elem is not None}")
        
        if title_elem is not None:
            print(f"Title: {title_elem.text[:50]}...")
            
except Exception as e:
    print(f"Parsing error: {e}")
    import traceback
    traceback.print_exc()