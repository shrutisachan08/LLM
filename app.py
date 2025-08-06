import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import parser, embedder, retriever, prompt_builder

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

# Paths
documents_folder = "documents"
faiss_index_path = "chunks_db/index.faiss"
os.makedirs("chunks_db", exist_ok=True)

# Parse and embed documents if FAISS not exists
@st.cache_data(show_spinner="Parsing & indexing documents...")
def process_docs():
    all_chunks = []
    for file in os.listdir(documents_folder):
        if file.endswith(".pdf"):
            text = parser.parse_pdf(os.path.join(documents_folder, file))
            chunks = embedder.chunk_text(text)
            all_chunks.extend(chunks)
    embeddings = embedder.embed_chunks(all_chunks)
    embedder.save_faiss_index(embeddings, faiss_index_path)
    return all_chunks

# Load chunks
all_chunks = process_docs()

# UI
st.title("📄 Insurance Policy AI Assistant")
st.markdown("Ask any query related to insurance policy clauses:")

query = st.text_area("📝 Enter your query here", height=100)

if st.button("🔍 Submit Query"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Retrieving relevant clauses and generating response..."):
            try:
                relevant_chunks = retriever.retrieve_clauses(query, all_chunks, faiss_index_path)
                prompt = prompt_builder.build_prompt(query, relevant_chunks)
                response = model.generate_content(prompt)
                st.success("✅ Response generated.")
                st.subheader("📦 Structured Response:")
                st.code(response.text, language="json")
            except Exception as e:
                st.error(f"❌ Error: {e}")
