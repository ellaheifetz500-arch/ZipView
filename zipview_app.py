
import streamlit as st
import zipfile
import os
import tempfile
from PIL import Image
import fitz  # PyMuPDF
import base64
import subprocess

st.set_page_config(
    page_title="ZipView – Preview ZIP without Extraction",
    page_icon="logo.png",
    layout="wide"
)

st.title("📦 ZipView – Preview ZIP without Extraction")
st.markdown("Upload a ZIP file to see its contents as thumbnails, PDFs, videos, and audio – no extraction needed.")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

def extract_audio_preview_ffmpeg(audio_path):
    try:
        preview_path = audio_path + "_preview.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-t", "10", "-acodec", "libmp3lame", preview_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(preview_path):
            with open(preview_path, "rb") as f:
                return f.read()
    except:
        pass
    return None

def is_pdf_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except:
        return False

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

                if is_pdf_file(file_path):
                    try:
                        st.markdown("🔍 Attempting PDF preview...")
                        doc = fitz.open(file_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        st.image(img_bytes)
                        st.markdown("✅ PDF preview displayed successfully.")
                    except Exception as e:
                        st.error(f"❌ Could not render PDF preview for {file}: {e}")
                    continue

                if ext in supported_video_exts:
                    try:
                        st.video(file_path)
                    except:
                        st.warning(f"Could not render video preview for {file}")
                    continue

                if ext in supported_audio_exts:
                    audio_data = extract_audio_preview_ffmpeg(file_path)
                    if audio_data:
                        st.audio(audio_data, format="audio/mp3")
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
