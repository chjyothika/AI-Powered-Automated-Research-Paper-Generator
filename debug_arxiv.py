import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.arxiv_fetcher import ArxivFetcher
import requests

# Test direct request first
print("Testing direct request...")
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
print(f"Status code: {response.status_code}")
print(f"Response length: {len(response.text)}")
print(f"First 500 chars: {response.text[:500]}")

# Test our fetcher
print("\nTesting our fetcher...")
fetcher = ArxivFetcher()
papers = fetcher.search_papers("neural networks", max_results=3)
print(f"Our fetcher found: {len(papers)} papers")