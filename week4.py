# week4.py
import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from PyPDF2 import PdfReader
from annoy import AnnoyIndex

# -------------------------
# Load API Key securely
# -------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# -------------------------
# Streamlit UI
# -------------------------
st.title("AI Study Assistant 🤖")
st.write("Upload a PDF and ask questions about its content!")

# Upload PDF
pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

# Initialize variables
pdf_text = ""
vector_index = None
vector_dim = 1536  # OpenAI embedding size

# -------------------------
# Process PDF
# -------------------------
if pdf_file:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"
    
    st.success("PDF loaded successfully! ✅")

    # Create Annoy index (example: simple split by sentences)
    sentences = pdf_text.split(". ")
    vector_index = AnnoyIndex(vector_dim, 'angular')

    # Create embeddings for each sentence
    for i, sentence in enumerate(sentences):
        if sentence.strip() == "":
            continue
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=sentence
        )
        embedding_vector = response.data[0].embedding
        vector_index.add_item(i, embedding_vector)
    
    vector_index.build(10)  # Number of trees
    st.info("PDF embeddings ready! You can now search.")

# -------------------------
# Search Bar
# -------------------------
user_query = st.text_input("Ask a question about the PDF:")

if st.button("Search") and user_query:
    if pdf_file:
        # Embed the user query
        query_embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=user_query
        ).data[0].embedding

        # Find top 3 similar sentences
        top_k = vector_index.get_nns_by_vector(query_embedding, 3)
        st.subheader("Top related content:")
        for idx in top_k:
            st.write(sentences[idx])
    else:
        st.warning("Please upload a PDF first!")





