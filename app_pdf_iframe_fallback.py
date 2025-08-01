import streamlit as st
import zipfile
from io import BytesIO
import tempfile
import base64
import os

st.title("PDF Viewer from ZIP (Fallback Method)")

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

                    # Save PDF to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(pdf_bytes)
                        tmp_path = tmp.name

                    # Encode PDF file to base64 to embed as iframe
                    with open(tmp_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)

                    os.remove(tmp_path)
