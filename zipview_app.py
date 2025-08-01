
import streamlit as st
import zipfile
import os
import base64

st.set_page_config(page_title="ZipView – Preview ZIP without Extraction", page_icon="📦")

st.markdown(f"<h1 style='display: flex; align-items: center; gap: 10px;'><img src='data:image/png;base64,{open('logo.png', 'rb').read().decode('latin1')}' width='40'/> ZipView – Preview ZIP without Extraction</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a ZIP file to see its contents as thumbnails without extracting.", type="zip")

def extract_and_list(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    return [os.path.join(extract_dir, name) for name in os.listdir(extract_dir)]

def render_file(file_path):
    filename = os.path.basename(file_path)
    st.markdown(f"**{filename}**")
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        st.image(file_path, use_column_width=True)
    elif filename.lower().endswith(".pdf"):
        st.markdown(f"<iframe src='data:application/pdf;base64,{base64.b64encode(open(file_path, 'rb').read()).decode()}' width='700' height='500'></iframe>", unsafe_allow_html=True)
    elif filename.lower().endswith((".mp4", ".webm")):
        with open(file_path, 'rb') as f:
            video_bytes = f.read()
            st.video(video_bytes)
    elif filename.lower().endswith((".mp3", ".wav", ".ogg")):
        with open(file_path, 'rb') as f:
            audio_bytes = f.read()
            st.audio(audio_bytes)
    else:
        st.text("No preview available for this file type.")

if uploaded_file:
    with open("temp.zip", "wb") as f:
        f.write(uploaded_file.getbuffer())
    extract_path = "extracted"
    os.makedirs(extract_path, exist_ok=True)
    extracted_files = extract_and_list("temp.zip", extract_path)
    for file in extracted_files:
        render_file(file)
