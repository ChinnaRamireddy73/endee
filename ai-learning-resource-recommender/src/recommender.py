from src.config import SEARCH_K
from src.dataset_loader import load_dataset
from src.embedding_generator import EmbeddingGenerator
from src.nlp_utils import preprocess_query
from src.vector_db import EndeeVectorDB

class AIRecommenderSystem:
    def __init__(self):
        self.db = EndeeVectorDB()
        self.encoder = EmbeddingGenerator()
        self.resources = load_dataset()
        
    def initialize_system(self):
        """Prepares the database by inserting all dataset items."""
        print("Starting System Initialization Sequence...")
        
        self.db.setup_collection()
        
        # Embed and Upload
        texts = [r["description"] for r in self.resources]
        embeddings = self.encoder.generate(texts)
        
        self.db.insert_docs(self.resources, embeddings)
        print("Initialization Sequence Completed successfully.\n")

    def recommend(self, query: str, category_filter: str = None) -> None:
        """
        Takes a natural language query, preprocesses it, and searches Endee.
        Applies requested category filtering.
        """
        print(f"\n[Raw Query]: '{query}'")
        
        # 1. NLP Preprocessing & Expansion
        processed_query = preprocess_query(query)
        print(f"[Processed NLP Query]: '{processed_query}'")
        
        # 2. Embedding Generation
        query_vector = self.encoder.generate_single(processed_query)
        
        # 3. Vector Database Similarity Search (Search deep so we can filter later)
        search_k = max(20, len(self.resources)) if category_filter else SEARCH_K
        results, search_time = self.db.search(query_vector, k=search_k)
        
        # 4. Optional Category Filtering post-search
        if category_filter:
            category_filter = category_filter.lower().strip()
            print(f"[Applying Filter]: Targeting category -> '{category_filter}'")
            filtered_results = [r for r in results if r.get('category', '').lower() == category_filter]
            results = filtered_results[:SEARCH_K]
            
        self._format_output(results, search_time)

    def _format_output(self, results: list[dict], search_time: float):
        """Displays beautiful formatted UI to standard output."""
        print(f"\nReturned {len(results)} optimal results in {search_time:.3f} seconds.")
        print("=" * 60)
        print("🌟 RECOMMENDED LEARNING RESOURCES 🌟")
        print("=" * 60)
        
        if not results:
            print("\nNo highly relevant records found for this category/query combination.\n")
            return
            
        for idx, result in enumerate(results, start=1):
            title = result.get('title', 'Unknown Title')
            category = result.get('category', 'General')
            score = result.get('_score', 0.0)
            desc = result.get('description', 'No description available')
            url = result.get('url', 'No URL provided')
            
            # Format nicely
            print(f"{idx}. {title}")
            print(f"   Category:    [{category.upper()}]")
            # Convert Endee Cosine Distance to a percentage-like certainty score
            print(f"   Relevancy:   {score:.4f} Score")
            print(f"   Description: {desc}")
            print(f"   Link:        {url}")
            print("-" * 60)
        print("\n")
