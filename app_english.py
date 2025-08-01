import streamlit as st
import zipfile
from io import BytesIO
from pdf2image import convert_from_bytes

st.title("📦 PDF Preview from ZIP")

uploaded_file = st.file_uploader("Upload a ZIP file containing PDF(s)", type="zip")

if uploaded_file:
    st.success("ZIP file uploaded successfully!")

    with zipfile.ZipFile(uploaded_file) as archive:
        st.write("📁 Files inside ZIP:")
        st.write(archive.namelist())

        pdf_files = [f for f in archive.namelist() if f.lower().endswith('.pdf')]
        st.write("📄 PDFs detected:")
        st.write(pdf_files)

        if not pdf_files:
            st.warning("No PDF files found in this ZIP.")
        else:
            for pdf_name in pdf_files:
                st.subheader(f"Preview: {pdf_name}")
                with archive.open(pdf_name) as file:
                    pdf_bytes = file.read()
                    images = convert_from_bytes(pdf_bytes)
                    for i, img in enumerate(images):
                        st.image(img, caption=f"Page {i+1}", use_column_width=True)
