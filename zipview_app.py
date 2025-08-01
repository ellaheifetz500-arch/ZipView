
import streamlit as st
import zipfile
import os
import io
from PIL import Image
from pdf2image import convert_from_bytes

st.set_page_config(page_title="ZipView Beta", layout="wide")
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
                image = Image.open(io.BytesIO(file_bytes))
                previews.append((file, image))

            elif file.lower().endswith(".pdf"):
                try:
                    images = convert_from_bytes(file_bytes, first_page=1, last_page=1)
                    if images:
                        previews.append((file, images[0]))
                except Exception:
                    pass

        if previews:
            st.subheader("📂 Previews")
            for name, img in previews:
                st.markdown(f"**{name}**")
                st.image(image, use_container_width=True)
        else:
            st.warning("No previewable files found in this ZIP.")
            st.markdown("""
            ---
            <div style='text-align: center; font-size: 0.8em; color: gray;'>
            © 2025 ZipView — Protected by U.S. and U.K. provisional application
            </div>
            """, unsafe_allow_html=True)

