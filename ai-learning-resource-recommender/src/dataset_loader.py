import json
import os
from src.config import DATASET_PATH

def load_dataset():
    """
    Loads and validates the learning resources JSON dataset.
    Ensures all required fields (title, description, url, category) are present.
    """
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Critical Error: Dataset not found at {DATASET_PATH}")
        
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            resources = json.load(f)
            
        valid_resources = []
        for i, res in enumerate(resources):
            if not isinstance(res, dict):
                print(f"Warning: Skipping invalid format at index {i}")
                continue
                
            title = res.get("title")
            desc = res.get("description")
            url = res.get("url")
            category = res.get("category", "Uncategorized")
            
            if not title or not desc or not url:
                print(f"Warning: Skipping incomplete record at index {i}: {res}")
                continue
                
            valid_resources.append({
                "title": title.strip(),
                "description": desc.strip(),
                "url": url.strip(),
                "category": category.strip()
            })
            
        print(f"Successfully loaded {len(valid_resources)} valid resources.")
        return valid_resources
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Critical Error: Dataset JSON is corrupted. {e}")
