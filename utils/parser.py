import fitz  # PyMuPDF
from docx import Document
from email import policy
from email.parser import BytesParser
import os

def parse_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Error parsing PDF: {e}"

def parse_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error parsing DOCX: {e}"

def parse_email(file_path):
    try:
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        return msg.get_body(preferencelist=('plain')).get_content()
    except Exception as e:
        return f"Error parsing Email: {e}"

def auto_parse(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext in [".eml", ".email"]:
        return parse_email(file_path)
    else:
        return "Unsupported file type"
