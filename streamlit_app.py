
import streamlit as st
from PIL import Image
import zipfile
import os
import base64

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction", page_icon="📦", layout="wide")

# Logo
st.image("logo.png", width=180)

st.title("ZipView – Preview ZIP Without Extraction")
st.write("Upload a ZIP file to see its contents as thumbnails without extracting.")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        file_list = zip_ref.namelist()
        for file in file_list:
            st.markdown(f"**{file}**")
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with zip_ref.open(file) as img_file:
                    image = Image.open(img_file)
                    st.image(image, caption=file, use_column_width=True)
            elif file.lower().endswith(".pdf"):
                st.markdown(f"📄 PDF preview not available in thumbnail mode. File: `{file}`")
            elif file.lower().endswith((".mp4", ".mov", ".avi")):
                st.video(zip_ref.open(file).read())
            elif file.lower().endswith((".mp3", ".wav")):
                st.audio(zip_ref.open(file).read())
