# handlers/pull_requests.py
import os
import requests

TOKEN = os.getenv("TOKEN")
HEADERS = {'Authorization': f'Bearer {TOKEN}'}


def get_pull_requests(state):
    """
    Example of return:
    [
        {"title": "Add useful stuff", "num": 56, "link": "https://github.com/boto/boto3/pull/56"},
        {"title": "Fix something", "num": 57, "link": "https://github.com/boto/boto3/pull/57"},
    ]
    """
    
    if state not in ("open", "closed", "all"):
        state = "open"
    
    headers = {
        "Accept": "application/vnd.github+json",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    params = {
        "state": state,
        "per_page": 100,
    }
    
    url = "https://api.github.com/repos/boto/boto3/pulls"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        pull_requests = []
        for pr in data:
            pull_requests.append({
                "num": pr.get("number"),
                "title": pr.get("title"),
                "link": pr.get("html_url"),
            })
        
        return pull_requests
        
    except Exception:
        return []