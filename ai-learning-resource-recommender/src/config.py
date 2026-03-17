import os

# Database Configuration
ENDEE_URL = "http://localhost:8080/api/v1"
COLLECTION_NAME = "learning_resources"

# Model Configuration
MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
SEARCH_K = 3

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "resources.json")
