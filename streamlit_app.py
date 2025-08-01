
import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import os
import tempfile
import mimetypes

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction")

# לוגו
logo = Image.open("logo.png")
st.image(logo, use_column_width=False, width=200)

# כותרת
st.markdown("<h1 style='text-align: center;'>ZipView – Preview ZIP Without Extraction</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a file (PDF, video, or audio)", type=["pdf", "mp4", "mov", "mp3", "wav"])

if uploaded_file:
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if uploaded_file.name.endswith(".pdf"):
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            st.markdown("### PDF Preview:")
            for page_num in range(min(5, len(doc))):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                st.image(pix.tobytes("png"))
        except Exception as e:
            st.error(f"Could not render PDF preview: {e}")
    elif mime_type and mime_type.startswith("video"):
        st.markdown("### Video Preview:")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmpfile:
            tmpfile.write(uploaded_file.read())
            st.video(tmpfile.name)
    elif mime_type and mime_type.startswith("audio"):
        st.markdown("### Audio Preview:")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmpfile:
            tmpfile.write(uploaded_file.read())
            st.audio(tmpfile.name)
    else:
        st.warning("Unsupported file type.")

# פוטר
st.markdown("""
<hr style="margin-top: 3em;">
<div style="text-align: center; font-size: 0.9em;">
    © 2025 ZipView — Protected by U.S. and U.K. Provisional Application
</div>
""", unsafe_allow_html=True)
