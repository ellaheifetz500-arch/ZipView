
import streamlit as st
import zipfile
import os
import io
import base64
from PIL import Image

st.set_page_config(page_title="ZipView – PDF + Video Preview", layout="wide")
st.title("📦 ZipView – Enhanced Viewer")

uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

def render_pdf_embed(file_bytes):
    b64 = base64.b64encode(file_bytes).decode()
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="500px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

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
                previews.append(("pdf", file, file_bytes))

            elif file.lower().endswith(".mp4"):
                previews.append(("video", file, file_bytes))

        if previews:
            st.subheader("📂 Previews")
            for preview_type, name, content in previews:
                st.markdown(f"**{name}**")
                if preview_type == "image":
                    st.image(content, use_container_width=True)
                elif preview_type == "video":
                    st.video(content)
                elif preview_type == "pdf":
                    render_pdf_embed(content)
        else:
            st.warning("No previewable files found in this ZIP.")
