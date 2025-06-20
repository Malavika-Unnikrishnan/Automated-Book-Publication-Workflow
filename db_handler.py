# db_handler.py

# db_handler.py (update reward_score only)



from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load model once (it's cached after first use)
reward_model = SentenceTransformer("all-MiniLM-L6-v2")










import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime,timezone
from uuid import uuid4
import hashlib

# ✅ Initialize DB + Embedding model
chroma_client = chromadb.Client()
EMBED_MODEL = embedding_functions.DefaultEmbeddingFunction()
COLLECTION_NAME = "chapter_versions"

def init_db():
    if COLLECTION_NAME not in [c.name for c in chroma_client.list_collections()]:
        chroma_client.create_collection(name=COLLECTION_NAME, embedding_function=EMBED_MODEL)
    return chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=EMBED_MODEL)

collection = init_db()

# ✅ Save any version of text with metadata
def save_version(version_type, text, metadata=None):
    doc_id = str(uuid4())
    metadata = metadata or {}
    
    metadata.update({
        "version_type": version_type,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"✅ Version '{version_type}' saved with ID: {doc_id}")

# ✅ Search top-k similar versions
def search_versions(query_text, top_k=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )
    return results

# ✅ Optional: reward-style score (cosine similarity proxy)
def reward_score(result_text, target_text):
    vec1 = reward_model.encode([result_text])[0]
    vec2 = reward_model.encode([target_text])[0]
    return float(cosine_similarity([vec1], [vec2])[0][0])
