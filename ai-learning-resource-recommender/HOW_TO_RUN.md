# How to Run the AI Learning Resource Recommender

This guide explains how to run the **AI Learning Resource Recommender V2** project step by step.

---

## 1. Prerequisites

Before running the project, make sure the following software is installed:

* Python **3.9 or higher**
* **Docker Desktop**
* Git

---

## 2. Clone the Repository

Clone the project repository:

```bash
git clone https://github.com/yourusername/endee.git
```

Navigate into the project directory:

```bash
cd endee
```

---

## 3. Start the Vector Database Server

The project uses the **Endee Vector Database** running inside Docker.

Start the server:

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker ps
```

The server should run on:

```
http://localhost:8080
```

---

## 4. Navigate to the Recommender Project

Move into the project folder:

```bash
cd ai-learning-resource-recommender
```

---

## 5. Install Dependencies

Install required Python libraries:

```bash
pip install -r requirements.txt
```

This installs libraries such as:

* sentence-transformers
* torch
* nltk
* requests

---

## 6. Run the Application

Run the main program:

```bash
python main.py
```

---

## 7. Use the System

The system will start an interactive search mode.

Example:

```
What would you like to learn? >> machine learning
Any specific category? >> AI
```

The system will return the **most relevant learning resources**.

---

## 8. Exit the Program

To exit the application:

```
exit
```

or

```
quit
```

---

## System Workflow

The recommender system works as follows:

User Query
↓
NLP Preprocessing
↓
Query Embedding Generation
↓
Vector Similarity Search (Endee DB)
↓
Ranking by Relevance Score
↓
Recommended Learning Resources

---

## Dataset

The learning resources are stored in:

```
dataset/resources.json
```

The dataset contains **60+ resources across multiple categories** including:

* AI
* CSE
* ECE
* Mathematics
* Physics
* Mechanical
* Civil
* English
* Telugu
* Aptitude

---

## Troubleshooting

If Docker is not running, start Docker Desktop and rerun:

```bash
docker compose up
```

If dependencies are missing, reinstall them:

```bash
pip install -r requirements.txt
```

---

## Author

AI Learning Resource Recommender V2
Semantic search system using NLP embeddings and the Endee Vector Database.
