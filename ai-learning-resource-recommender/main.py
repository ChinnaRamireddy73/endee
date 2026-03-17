import sys
import argparse
from src.recommender import AIRecommenderSystem

def main():
    parser = argparse.ArgumentParser(description="AI Learning Resource Recommender V2")
    parser.add_argument("--skip-init", action="store_true", help="Skip initializing Endee and generating new embeddings (useful if DB is already loaded)")
    parser.add_argument("--query", "-q", type=str, help="Skip interactive mode and search immediately")
    parser.add_argument("--category", "-c", type=str, help="Optionally filter search results by a specific Category (e.g. 'CSE', 'AI')")
    
    args = parser.parse_args()

    print("\n==============================================")
    print("🎓 AI Learning Resource Recommender V2 (Endee VDB) 🎓")
    print("==============================================\n")
    
    try:
        # Initialize Core Pipeline
        recommender = AIRecommenderSystem()
        
        if not args.skip_init:
            recommender.initialize_system()
        else:
            print("Skipping Dataset Embedding Initialization...\n")
            
        # Non-Interactive Mode
        if args.query:
            recommender.recommend(args.query, category_filter=args.category)
            sys.exit(0)
            
        # Interactive Mode
        print("\nEntering Interactive Search Mode (Type 'exit' or 'quit' to leave)\n")
        while True:
            try:
                user_input = input("\nWhat would you like to learn? >> ")
                if not user_input.strip():
                    continue
                if user_input.strip().lower() in ["exit", "quit"]:
                    print("Exiting Recommender... Goodbye!\n")
                    break
                    
                # Ask optionally for a category filter on the fly
                filter_input = input("Any specific category? (Press Enter to skip) >> ")
                selected_cat = filter_input.strip() if filter_input.strip() else None
                
                recommender.recommend(user_input, category_filter=selected_cat)
                
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        print(f"\n[FATAL ERROR] Sequence Halted: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()