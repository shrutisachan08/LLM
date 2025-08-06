import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_clauses(query, chunks, index_path="chunks_db/index.faiss", k=3):
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found at {index_path}")
    
    index = faiss.read_index(index_path)
    query_vec = model.encode([query])
    
    # Convert to float32 and numpy array
    query_vec = np.array(query_vec).astype("float32")
    
    # Search for top-k results
    _, indices = index.search(query_vec, k)

    # Filter out-of-bound indices (edge case protection)
    matched_chunks = []
    for i in indices[0]:
        if 0 <= i < len(chunks):
            matched_chunks.append(chunks[i])
    
    return matched_chunks
