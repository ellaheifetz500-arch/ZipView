
import streamlit as st
from PIL import Image
import zipfile
import io
import base64

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction", page_icon="📦")

st.title("📦 ZipView – Preview ZIP Without Extraction")
st.write("Upload a ZIP file to preview images, PDFs, videos, and audio without extracting.")

def display_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.components.v1.html(pdf_display, height=1000, scrolling=True)

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as zip_ref:
        for file in zip_ref.namelist():
            st.markdown(f"### 📄 {file}")
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                img_bytes = zip_ref.read(file)
                st.image(Image.open(io.BytesIO(img_bytes)), caption=file, use_container_width=True)
            elif file.lower().endswith(".pdf"):
                pdf_bytes = zip_ref.read(file)
                display_pdf(pdf_bytes)
            elif file.lower().endswith((".mp4", ".mov")):
                st.video(io.BytesIO(zip_ref.read(file)))
            elif file.lower().endswith((".mp3", ".wav")):
                st.audio(io.BytesIO(zip_ref.read(file)))
            else:
                st.info("No preview available for this file type.")
                st.markdown("""
                ---
               st.markdown("""
---
<div style='text-align: center; font-size: 0.8em; color: gray;'>
© 2025 ZipView — Protected by U.S. and U.K. provisional application
</div>
""", unsafe_allow_html=True)
