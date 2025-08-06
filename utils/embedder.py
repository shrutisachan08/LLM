from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json

# Load model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=100):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_chunks(chunks):
    return model.encode(chunks, show_progress_bar=True)

def save_faiss_index(embeddings, path="chunks_db/index.faiss"):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)

def save_chunks(chunks, path="chunks_db/chunks.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(chunks, f, indent=2)

def load_chunks(path="chunks_db/chunks.json"):
    with open(path, "r") as f:
        return json.load(f)
