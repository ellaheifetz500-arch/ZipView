
import streamlit as st
import zipfile
import os
import io
from PIL import Image
import PyPDF2
import base64

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction", page_icon="📦")

st.markdown("""
    <style>
        .logo-img {
            width: 80px;
        }
        .logo-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .logo-title {
            font-size: 2rem;
            font-weight: bold;
        }
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{0}" class="logo-img"/>
        <span class="logo-title">ZipView – Preview ZIP Without Extraction</span>
    </div>
""".format(base64.b64encode(open("logo.png", "rb").read()).decode()), unsafe_allow_html=True)

st.subheader("Upload a ZIP file to see its contents as thumbnails without extracting.")
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        for file in zip_ref.namelist():
            st.write(f"**{file}**")
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_data = zip_ref.read(file)
                st.image(Image.open(io.BytesIO(image_data)))
            elif file.lower().endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(zip_ref.read(file)))
                st.write("📄 PDF Preview:")
                st.text(pdf_reader.pages[0].extract_text())
            elif file.lower().endswith(('.mp4', '.mov')):
                video_bytes = zip_ref.read(file)
                st.video(io.BytesIO(video_bytes))
            elif file.lower().endswith(('.mp3', '.wav')):
                audio_bytes = zip_ref.read(file)
                st.audio(io.BytesIO(audio_bytes))
            else:
                st.info("No preview available for this file type.")
