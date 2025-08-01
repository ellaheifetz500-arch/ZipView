import streamlit as st
import zipfile
from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image

st.title("PDF Preview from ZIP (First Page Only)")

uploaded_file = st.file_uploader("Upload a ZIP file containing PDF(s)", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as archive:
        pdf_files = [f for f in archive.namelist() if f.lower().endswith(".pdf")]

        if not pdf_files:
            st.warning("No PDF files found in the ZIP.")
        else:
            for pdf_name in pdf_files:
                st.subheader(f"📄 {pdf_name}")
                with archive.open(pdf_name) as pdf_file:
                    pdf_bytes = pdf_file.read()
                    try:
                        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                        page = doc.load_page(0)  # First page
                        pix = page.get_pixmap(dpi=150)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        st.image(img, caption="Page 1 Preview", use_column_width=True)
                        doc.close()
                    except Exception as e:
                        st.error(f"Failed to render preview: {e}")
