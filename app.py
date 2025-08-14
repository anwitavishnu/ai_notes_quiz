import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

# Load API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI PDF Notes & Quiz Generator", layout="centered")
st.title("📄 AI PDF Notes & Quiz Generator")
st.write("Upload a PDF and get AI-generated **notes** and **quiz questions**.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

def extract_text_from_pdf(file):
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text

def generate_notes(text):
    prompt = f"Summarize the following text into clear, concise study notes:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_quiz(text):
    prompt = f"Create 5 multiple-choice questions with 4 options each (mark the correct option) from the following text:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Generating notes..."):
        notes = generate_notes(extracted_text)

    with st.spinner("Generating quiz..."):
        quiz = generate_quiz(extracted_text)

    st.subheader("📝 AI-Generated Notes")
    st.write(notes)

    st.subheader("❓ AI-Generated Quiz")
    st.write(quiz)

