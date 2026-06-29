import pandas as pd
import requests

def summarize_abstract(abstract):
    if not abstract or abstract == "":
        return "No abstract available"
    
    url = "https://api.anthropic.com/v1/messages"
    
    headers = {
        "x-api-key": "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",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 150,
        "messages": [
            {
                "role": "user",
                "content": f"Summarize this research paper abstract in 2-3 sentences:\n\n{abstract}"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=body)
    result = response.json()
    return result["content"][0]["text"]

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