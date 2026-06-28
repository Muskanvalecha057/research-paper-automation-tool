import requests
import pandas as pd

def fetch_papers(keyword, max_results=10):
    print(f"Searching papers for: {keyword}")
    
    url = "https://api.openalex.org/works"
    
    params = {
        "search": keyword,
        "per-page": max_results,
        "select": "title,authorships,publication_year,abstract_inverted_index"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    papers = []
    for paper in data["results"]:
        authors = ", ".join([
            a["author"]["display_name"] 
            for a in paper.get("authorships", [])
        ])
        papers.append({
            "Title": paper.get("title", ""),
            "Year": paper.get("publication_year", ""),
            "Authors": authors,
        })
    
    df = pd.DataFrame(papers)
    df.to_csv("papers.csv", index=False)
    print(f"Done! {len(papers)} papers saved to papers.csv")

keyword = input("Enter your research topic: ")
fetch_papers(keyword)