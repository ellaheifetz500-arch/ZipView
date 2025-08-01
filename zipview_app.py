
import streamlit as st
import zipfile
import os
import tempfile
from PIL import Image
import fitz  # PyMuPDF
import base64

st.set_page_config(
    page_title="Preview ZIP Without Extraction",
    page_icon="logo.png",
    layout="wide"
)

st.markdown("## ZipView – Preview ZIP Without Extraction")
st.markdown("Upload a ZIP file to see its contents as thumbnails without extracting.")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_path = os.path.join(tmpdirname, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        for root, dirs, files in os.walk(tmpdirname):
            for file in files:
                file_path = os.path.join(root, file)
                ext = file.lower().split('.')[-1]

                st.markdown(f"**{file}**")

                if ext in ["png", "jpg", "jpeg", "webp"]:
                    image = Image.open(file_path)
                    st.image(image, use_container_width=True)

                elif ext == "pdf":
                    try:
                        doc = fitz.open(file_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        st.image(img_bytes)
                    except:
                        st.warning(f"Could not render PDF preview for {file}")

                elif ext in ["mp4", "mov", "avi"]:
                    with open(file_path, "rb") as video_file:
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                else:
                    with open(file_path, "r", errors="ignore") as txt_file:
                        content = txt_file.read(500)
                        st.code(content)
