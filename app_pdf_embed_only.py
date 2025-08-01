import streamlit as st
import zipfile
from io import BytesIO

st.title("📄 View PDF Files from ZIP (No Poppler)")

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
                    st.download_button("Download PDF", pdf_bytes, file_name=pdf_name)
                    st.pdf(BytesIO(pdf_bytes))
