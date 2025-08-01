
import streamlit as st
import zipfile
import os
import io
import base64
from PIL import Image
from pdf2image import convert_from_bytes

st.set_page_config(page_title="ZipView – Beta+", layout="wide")
st.title("📦 ZipView – Preview ZIP Files Without Extracting")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        file_list = zip_ref.namelist()
        previews = []

        for file in file_list:
            if file.endswith("/"):
                continue
            file_bytes = zip_ref.read(file)

            if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                try:
                    image = Image.open(io.BytesIO(file_bytes))
                    previews.append(("image", file, image))
                except:
                    pass

            elif file.lower().endswith(".pdf"):
                try:
                    images = convert_from_bytes(file_bytes, first_page=1, last_page=1)
                    if images:
                        previews.append(("pdf", file, images[0]))
                except Exception:
                    st.warning(f"Could not render PDF preview for {file}.")

            elif file.lower().endswith(".mp4"):
                try:
                    previews.append(("video", file, file_bytes))
                except:
                    pass

        if previews:
            st.subheader("📂 Previews")
            for preview_type, name, content in previews:
                st.markdown(f"**{name}**")
                if preview_type == "image" or preview_type == "pdf":
                    st.image(content, use_container_width=True)
                elif preview_type == "video":
                    st.video(content)
        else:
            st.warning("No previewable files found in this ZIP.")
