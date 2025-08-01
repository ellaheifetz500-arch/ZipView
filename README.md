# Streamlit PDF Viewer (No Poppler, iframe Fallback)

This version of the app displays PDF files embedded via HTML iframe instead of using `st.pdf()`. It avoids the "No previewable files" error on Streamlit Cloud.

## ✅ Features
- Upload a ZIP file with PDF(s)
- Display each PDF using iframe
- No poppler required
- No PDF viewer dependencies

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app_pdf_iframe_fallback.py
```
