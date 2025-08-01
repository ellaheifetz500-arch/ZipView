import streamlit as st
import zipfile
from io import BytesIO
from pdf2image import convert_from_bytes

st.title("📦 ZIP PDF Previewer")

uploaded_file = st.file_uploader("העלה קובץ ZIP עם PDF", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as archive:
        pdf_files = [f for f in archive.namelist() if f.endswith(".pdf")]

        if not pdf_files:
            st.warning("לא נמצאו קבצי PDF בתוך קובץ ה-ZIP.")
        else:
            for pdf_name in pdf_files:
                st.header(f"📄 {pdf_name}")
                with archive.open(pdf_name) as pdf_file:
                    pdf_bytes = pdf_file.read()
                    try:
                        images = convert_from_bytes(pdf_bytes)
                        for i, img in enumerate(images):
                            st.image(img, caption=f"עמוד {i+1}", use_column_width=True)
                    except Exception as e:
                        st.error(f"שגיאה בעת עיבוד {pdf_name}: {e}")
