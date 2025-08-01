# PDF Viewer from ZIP (Streamlit App)

This Streamlit app allows users to upload a ZIP file that contains one or more PDF files.
Each PDF is displayed directly in the browser using Streamlit's `st.pdf()` — no external dependencies like `poppler` are required.

## ✅ Features
- Upload ZIP file with PDF(s)
- View entire PDF files in-browser
- No `poppler` required
- Download button for each PDF

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app_pdf_embed_only.py
```

## 📦 Requirements
- streamlit >= 1.10
