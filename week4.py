# week4.py

import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader
from annoy import AnnoyIndex

# --------------------------
# Load OpenAI API key
# --------------------------
if "OPENAI_API_KEY" in st.secrets:
    # Running on Streamlit Cloud
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    # Local testing
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# --------------------------
# Streamlit Interface
# --------------------------
st.title("AI Study Assistant 🤖")

st.write("You can ask questions directly or upload a PDF and ask questions from it.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF (optional)", type=["pdf"])

# Text input
user_question = st.text_input("Ask a study question:")

# --------------------------
# Process PDF if uploaded
# --------------------------
pdf_text = ""
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"
    st.success("PDF uploaded successfully!")

# --------------------------
# Search/Answer Function
# --------------------------
def ask_question(question, context=""):
    messages = []
    if context:
        messages.append({"role": "system", "content": f"Use this context: {context}"})
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    return answer

# --------------------------
# Button to ask
# --------------------------
if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question!")
    else:
        # If PDF uploaded, use its content as context
        answer = ask_question(user_question, pdf_text)
        st.subheader("Answer:")
        st.write(answer)







