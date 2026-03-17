import json
import requests
import msgpack
import time
from src.config import ENDEE_URL, COLLECTION_NAME, EMBEDDING_DIM

class EndeeVectorDB:
    def __init__(self):
        self.health_check()
        
    def health_check(self):
        """Verifies the Endee Database is accessible."""
        try:
            response = requests.get(f"{ENDEE_URL}/health")
            if response.status_code == 200:
                print("Database Health: OK (Connected to Endee)")
                return True
        except requests.exceptions.ConnectionError:
            pass
        raise ConnectionError(f"CRITICAL: Cannot reach Endee VectorDB at {ENDEE_URL}. Please ensure Docker container is running.")

    def setup_collection(self):
        """Creates the Endee collection, replacing it if it already exists."""
        # Check if index exists
        try:
            response = requests.get(f"{ENDEE_URL}/index/list")
            if response.status_code == 200:
                indexes = response.json().get("indexes", [])
                for idx in indexes:
                    if idx.get("name") == COLLECTION_NAME:
                        print(f"Collection '{COLLECTION_NAME}' already exists. Recreating it to ensure fresh data...")
                        # Delete endpoint returns simple text, avoiding .json() issues
                        requests.delete(f"{ENDEE_URL}/index/{COLLECTION_NAME}/delete")
                        time.sleep(1) 
                        break
        except Exception as e:
            print(f"Warning checking indexes: {e}")
                    
        print(f"Creating collection '{COLLECTION_NAME}'...")
        payload = {
            "index_name": COLLECTION_NAME,
            "dim": EMBEDDING_DIM,
            "space_type": "cosine",
        }
        
        response = requests.post(f"{ENDEE_URL}/index/create", json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to create collection: {response.text}")
            
    def insert_docs(self, resources: list[dict], embeddings: list[list[float]]):
        """Upserts vectors with their associated metadata payloads."""
        if len(resources) != len(embeddings):
            raise ValueError("Mismatched dimensions between text and embeddings.")
            
        vectors_payload = []
        for i, (resource, emb) in enumerate(zip(resources, embeddings)):
            vectors_payload.append({
                "id": str(i + 1),
                "vector": emb,
                "meta": json.dumps(resource) # Serialize full object for later recovery
            })
            
        print(f"Inserting {len(vectors_payload)} vectors into Endee...")
        response = requests.post(
            f"{ENDEE_URL}/index/{COLLECTION_NAME}/vector/insert",
            json=vectors_payload
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Failed to insert vectors: {response.text}")
        print("Data successfully committed to Database.\n")
            
    def search(self, query_vector: list[float], k: int = 3) -> tuple[list[dict], float]:
        """Performs nearest-neighbor search, explicitly handling MessagePack binary response arrays."""
        payload = {
            "k": k,
            "vector": query_vector
        }
        
        start_time = time.time()
        response = requests.post(
            f"{ENDEE_URL}/index/{COLLECTION_NAME}/search",
            json=payload
        )
        search_time = time.time() - start_time
        
        if response.status_code != 200:
            raise RuntimeError(f"Search failed: {response.text}")
            
        # Parse the custom MsgPack binary array native to Endee's C++ Backend
        try:
            data = msgpack.unpackb(response.content, raw=False)
            
            # The search API returns an array of arrays representing the structs:
            # r[0] = similarity (float)
            # r[1] = id (string)
            # r[2] = user defined metadata (bytes string of our JSON)
            # r[3]... etc
            parsed_results = []
            
            # Accommodate both direct array of results and dict{"results": array} structures
            items = data.get("results", data) if isinstance(data, dict) else data

            for item in items:
                # Based on the binary extraction debug log we retrieved earlier:
                # [0.080..., '59', b'{"title": "...", ...}']
                if not isinstance(item, list) or len(item) < 3:
                    continue
                    
                similarity = item[0]
                meta_bytes = item[2]
                
                if isinstance(meta_bytes, bytes):
                    meta_str = meta_bytes.decode('utf-8')
                else:
                    meta_str = str(meta_bytes)
                    
                meta_json = json.loads(meta_str)
                meta_json["_score"] = float(similarity)
                parsed_results.append(meta_json)
                
            return parsed_results, search_time
            
        except Exception as e:
            raise RuntimeError(f"Failed to decode search response from Endee: {e}")
