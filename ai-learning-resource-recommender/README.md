# AI Learning Resource Recommender V2

## Project Overview
This project is an advanced, modular AI-powered Learning Resource Recommender application. It accepts user questions about learning subjects, converts their natural language query into vector embeddings using standard NLP techniques, and performs a semantic search against a diverse multi-category dataset of learning resources to recommend the most relevant materials.

## Problem Statement
Traditional exact-match keyword searching fails when users search for concepts using different terminology. A student looking for "OOP" might miss a resource titled "Advanced Python Object Oriented Programming". This project solves this semantic gap by using AI text-embeddings, Natural Language Processing, and an advanced vector database to recommend resources based on contextual similarity rather than keyword matching.

## System Architecture

The application has been completely modularized natively into separated concerns under `src/`:

1. **Config (`src/config.py`)**: Centralized application settings.
2. **Dataset Loader (`src/dataset_loader.py`)**: Safely parses `dataset/resources.json` handling format invalidations and strict schema bindings (`Title`, `URL`, `Description`, `Category`).
3. **NLP Preprocessor (`src/nlp_utils.py`)**: Uses `NLTK` to remove stopwords, lowercase queries, and implements a Domain Keyword Expansion dictionary (e.g., transforming "OOP" to "Object Oriented Programming" under the hood before vector generation).
4. **Text Embedding Model (`src/embedding_generator.py`)**: Uses the `all-MiniLM-L6-v2` model natively via isolating initialization wrapper to cleanly transform descriptions into 384-dimensional dense vectors.
5. **Vector Database (`src/vector_db.py`)**: **Endee** running locally in Docker (`http://localhost:8080`) handles the high-performance storage and Nearest Neighbor similarity searching natively decoding binary `MessagePack` arrays to reconstruct result payloads natively.
6. **Recommender (`src/recommender.py`)**: Orchestrates the modules allowing end-to-end processing with runtime Category Filtering logic and normalized relevancy scoring.

## Dataset Description
The dataset is located in `dataset/resources.json`. It is a JSON array of 60+ objects representing learning modules. Each module has:
- `title`: The name of the resource.
- `description`: The textual body defining what the subject is. (This is what gets converted to a vector).
- `url`: A reference link for the resource.
- `category`: Domain identifier (e.g. `AI`, `CSE`, `ECE`, `Mathematics`)

## Setup Instructions
Make sure you have Docker Desktop installed and Python 3.9+.

### 1. Start Endee Server
This project assumes you have the Endee GitHub repository cloned and running on port 8080 via Docker.
Navigate to your Endee repo root directory:
```bash
docker compose up -d
```

### 2. Install Project Dependencies
Navigate to this project folder (`ai-learning-resource-recommender`) and install the newly required Python packages (including NLP libraries):
```bash
pip install -r requirements.txt
```

## Running the Project
Once Endee is running, you can engage the system in multiple ways:

**Interactive Mode**:
```bash
python main.py
```

**Direct NLP Query**:
```bash
python main.py -q "I want to learn about ML and neural networks"
```

**Category-Isolated Query**:
```bash
python main.py -q "oop concepts" -c "CSE"
```

## Example Output
```
Returned 3 optimal results in 0.009 seconds.
============================================================
🌟 RECOMMENDED LEARNING RESOURCES 🌟
============================================================
1. Machine Learning Crash Course
   Category:    [AI]
   Relevancy:   0.6554 Score
   Description: Learn ML concepts with real examples
   Link:        https://developers.google.com/machine-learning/crash-course
------------------------------------------------------------
```
