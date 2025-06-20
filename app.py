import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from appointment_form import show_appointment_form


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

  # Replace with your Gemini API key

def get_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_into_chunks(text, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def ask_gemini_with_context(context, question):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )
    prompt = f"""Answer the following question based only on the context below.

Context:
{context}

Question:
{question}
"""
    return llm.invoke(prompt).content

st.set_page_config(page_title="Gemini PDF QA & Appointment Form", layout="centered")
st.title("Ask Questions from PDF & Book Appointment")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Reading and processing PDF..."):
        text = get_pdf_text(uploaded_file)
        chunks = split_into_chunks(text)
        st.success(f"PDF loaded with {len(chunks)} chunks")

    question = st.text_input("Ask a question about the PDF:")

    if question:
        with st.spinner("Gemini is thinking..."):
            full_context = "\n\n".join(chunks[:5])
            answer = ask_gemini_with_context(full_context, question)
            st.markdown("### Gemini's Answer")
            st.write(answer)

    st.markdown("---")
    show_appointment_form()
