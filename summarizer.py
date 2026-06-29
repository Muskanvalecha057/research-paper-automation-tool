import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def summarize_abstract(abstract):
    if not abstract or abstract == "":
        return "No abstract available"
    
    api_key = os.getenv("GROQ_API_KEY")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"Summarize this research paper abstract in 2-3 sentences:\n\n{abstract}"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=body)
    result = response.json()
    return result["choices"][0]["message"]["content"]

def summarize_papers():
    df = pd.read_csv("papers.csv")
    print(f"Summarizing {len(df)} papers...")
    
    summaries = []
    for i, row in df.iterrows():
        print(f"Paper {i+1}/{len(df)}: {row['Title'][:50]}...")
        summary = summarize_abstract(row.get("Abstract", ""))
        summaries.append(summary)
    
    df["Summary"] = summaries
    df.to_csv("papers_summarized.csv", index=False)
    print("Done! Saved to papers_summarized.csv")

summarize_papers()