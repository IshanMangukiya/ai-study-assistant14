import streamlit as st
import os
import openai
from PyPDF2 import PdfReader
from annoy import AnnoyIndex

# --------------------------
# Load API Key
# --------------------------
api_key = None

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    except ModuleNotFoundError:
        pass

if api_key is None:
    st.error("OpenAI API key not found!")
else:
    openai.api_key = api_key

# --------------------------
# Streamlit UI
# --------------------------
st.title("AI Study Assistant 🤖")
st.write("You can ask questions directly or upload a PDF and ask questions from it.")

uploaded_file = st.file_uploader("Upload a PDF (optional)", type=["pdf"])
user_question = st.text_input("Ask a study question:")

pdf_text = ""
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"
    st.success("PDF uploaded successfully!")

def ask_question(question, context=""):
    messages = []
    if context:
        messages.append({"role": "system", "content": f"Use this context: {context}"})
    messages.append({"role": "user", "content": question})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question!")
    else:
        answer = ask_question(user_question, pdf_text)
        st.subheader("Answer:")
        st.write(answer)










