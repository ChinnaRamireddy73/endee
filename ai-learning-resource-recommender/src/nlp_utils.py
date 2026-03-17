import nltk
from nltk.corpus import stopwords
import string

# Download stopwords silently if not present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Common mappings for computer science terminology expansion
DOMAIN_EXPANSIONS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "ai": "artificial intelligence",
    "oop": "object oriented programming",
    "os": "operating systems",
    "dbms": "database management systems",
    "ui": "user interface",
    "ux": "user experience",
    "cse": "computer science engineering",
    "ece": "electronics and communication",
    "ds": "data structures"
}

def preprocess_query(query: str) -> str:
    """
    Applies NLP techniques to enhance the querying potential of raw text:
    1. Lowercasing
    2. Punctuation removal
    3. Query expansion using domain knowledge
    4. Stopword removal
    """
    # Lowercase and handle punctuation
    query = query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    words = query.split()
    
    # Expand and filter
    stop_words = set(stopwords.words('english'))
    processed_words = []
    
    for word in words:
        if word in stop_words:
            continue
            
        # Check dictionary expansion
        if word in DOMAIN_EXPANSIONS:
            expanded = DOMAIN_EXPANSIONS[word]
            processed_words.extend(expanded.split())
        else:
            processed_words.append(word)
            
    processed_query = " ".join(processed_words)
    return processed_query
