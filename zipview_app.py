
import streamlit as st
import zipfile
import os
import tempfile
from PIL import Image
import fitz  # PyMuPDF
import base64
import subprocess
from pydub import AudioSegment
import io

st.set_page_config(
    page_title="Preview ZIP Without Extraction",
    page_icon="logo.png",
    layout="wide"
)

st.title("📦 Preview ZIP Without Extraction")
st.markdown("Upload a ZIP file to see its contents as thumbnails, PDFs, videos, and audio – no extraction needed.")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

def extract_audio_preview(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        preview = audio[:10000]  # 10 seconds
        buf = io.BytesIO()
        preview.export(buf, format="mp3")
        return buf.getvalue()
    except:
        return None

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_path = os.path.join(tmpdirname, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        supported_image_exts = ["png", "jpg", "jpeg", "webp"]
        supported_video_exts = ["mp4", "mov", "avi"]
        supported_audio_exts = ["mp3", "wav", "m4a"]
        supported_text_exts = ["txt"]
        supported_pdf_exts = ["pdf"]

        for root, dirs, files in os.walk(tmpdirname):
            for file in files:
                file_path = os.path.join(root, file)
                ext = file.lower().split('.')[-1]
                rel_path = os.path.relpath(file_path, tmpdirname)

                if rel_path.startswith(".preview") or file.startswith("."):
                    continue

                st.markdown(f"**{rel_path}**")

                if ext in supported_image_exts:
                    try:
                        image = Image.open(file_path)
                        st.image(image, use_container_width=True)
                    except:
                        st.warning(f"Could not display image: {file}")
                    continue

                if ext in supported_pdf_exts:
                    try:
                        doc = fitz.open(file_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        st.image(img_bytes)
                    except:
                        st.warning(f"Could not render PDF preview for {file}")
                    continue

                if ext in supported_video_exts:
                    try:
                        st.video(file_path)
                    except:
                        st.warning(f"Could not render video preview for {file}")
                    continue

                if ext in supported_audio_exts:
                    audio_preview = extract_audio_preview(file_path)
                    if audio_preview:
                        st.audio(audio_preview, format="audio/mp3")
                    else:
                        st.warning(f"Could not render audio preview for {file}")
                    continue

                if ext in supported_text_exts:
                    try:
                        with open(file_path, "r", errors="ignore") as txt_file:
                            content = txt_file.read(500)
                            st.code(content)
                    except:
                        st.warning(f"Could not read file: {file}")
                    continue

                st.info("No preview available for this file type.")
