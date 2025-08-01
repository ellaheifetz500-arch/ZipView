
import streamlit as st
from PIL import Image
import fitz  # PyMuPDF

st.set_page_config(page_title="ZipView – Preview ZIP Without Extraction")

# לוגו
logo = Image.open("logo.png")
st.image(logo, use_column_width=False, width=200)

# כותרת
st.markdown("<h1 style='text-align: center;'>ZipView – Preview ZIP Without Extraction</h1>", unsafe_allow_html=True)

# הדגמה לתצוגת PDF
import fitz  # PyMuPDF
import streamlit as st

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)  # עמוד ראשון
        pix = page.get_pixmap()
        st.image(pix.tobytes("png"))  # מציג תמונה של עמוד ה־PDF
    except Exception as e:
        st.error(f"Could not render PDF preview: {e}")
