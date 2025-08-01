
import streamlit as st
import zipfile
import os
import io
from PIL import Image
import PyPDF2
import base64

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction", page_icon="📦")

# Load logo
with open("logo.jpg", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <img src='data:image/jpg;base64,{logo_base64}' width='60'/>
        <h1>ZipView – Preview ZIP Without Extraction</h1>
    </div>
""", unsafe_allow_html=True)

st.write("Upload a ZIP file to preview its contents without extraction.")

uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as zip_ref:
        for file in zip_ref.namelist():
            st.markdown(f"**README.md**")
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_data = zip_ref.read(file)
                st.image(Image.open(io.BytesIO(image_data)))
            elif file.lower().endswith(".pdf"):
                pdf_file = io.BytesIO(zip_ref.read(file))
                try:
                    reader = PyPDF2.PdfReader(pdf_file)
                    text = reader.pages[0].extract_text()
                    st.text(text if text else "[No extractable text]")
                except:
                    st.warning("Couldn't preview this PDF.")
            elif file.lower().endswith(('.mp4', '.mov')):
                video_bytes = zip_ref.read(file)
                st.video(io.BytesIO(video_bytes))
            elif file.lower().endswith(('.mp3', '.wav')):
                audio_bytes = zip_ref.read(file)
                st.audio(io.BytesIO(audio_bytes))
            else:
                st.info("No preview available for this file type.")
