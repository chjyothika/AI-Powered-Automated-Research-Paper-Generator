import requests
import xml.etree.ElementTree as ET
import time

def fetch_arxiv_papers(query, max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }
    
    headers = {
        "User-Agent": "ScopusReadyPaperGenerator/1.0 (academic project)"
    }
    
    response = requests.get(base_url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    
    return response.text

def parse_arxiv_xml(xml_data):
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    papers = []
    
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()
        published = entry.find("atom:published", ns).text[:10]
        
        authors = [
            author.find("atom:name", ns).text
            for author in entry.findall("atom:author", ns)
        ]
        
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib["href"]
        
        papers.append({
            "title": title,
            "authors": authors,
            "published": published,
            "pdf": pdf_link,
            "summary": summary
        })
    
    return papers

# Test the working code
print("Testing working arXiv code...")
time.sleep(3)  # polite delay

xml_data = fetch_arxiv_papers("neural networks", max_results=3)
papers = parse_arxiv_xml(xml_data)

print(f"Found {len(papers)} papers")
for i, p in enumerate(papers):
    print(f"{i+1}. Title: {p['title'][:60]}...")
    print(f"   Authors: {len(p['authors'])} authors")
    print(f"   Published: {p['published']}")
    print("-" * 40)