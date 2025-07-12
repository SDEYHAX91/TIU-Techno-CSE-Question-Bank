# app.py
import streamlit as st
from pathlib import Path
import datetime

# ---------- Config ----------
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)          # create the folder if it isn't there

st.set_page_config(page_title="Question‑Paper Bank", page_icon="📚")
st.title("📚 Previous‑Semester Question Papers")

# ---------- Upload section ----------
st.header("➕ Upload a new paper (PDF)")
uploaded_file = st.file_uploader(
    "Choose a PDF file", type="pdf", label_visibility="collapsed"
)

if 'last_uploaded' not in st.session_state:
    st.session_state['last_uploaded'] = None

if uploaded_file:
    if uploaded_file.name != st.session_state['last_uploaded']:
        # Only save if it's a new file
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = UPLOAD_DIR / f"{timestamp}_{uploaded_file.name}"
        save_path.write_bytes(uploaded_file.read())
        st.session_state['last_uploaded'] = uploaded_file.name
        st.success(f"Uploaded **{uploaded_file.name}**")
    else:
        st.info("This file is already uploaded in this session.")

# ---------- List & download section ----------
st.header("📂 Available papers")
pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))

if pdf_files:
    for pdf in pdf_files:
        with pdf.open("rb") as f:
            st.download_button(
    label=f"📄 {pdf.name.split('_',1)[-1]}",
    data=f.read(),
    file_name=pdf.name.split('_',1)[-1],
    mime="application/pdf",
    key=pdf.name  # 👈 this makes each button unique
)

else:
    st.info("No papers uploaded yet. Add one above!")
