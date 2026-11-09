from PyPDF2 import PdfReader
import docx


def extract_text(file, file_type):
    """
    Safely extract text from PDF or DOCX files.
    """

    try:
        if file_type.lower() == "pdf":
            return extract_pdf(file)

        elif file_type.lower() == "docx":
            return extract_docx(file)

        else:
            return "Unsupported file format"

    except Exception as e:
        return f"[Error reading document: {str(e)}]"


# -----------------------------
# PDF EXTRACTOR (SAFE)
# -----------------------------
def extract_pdf(file):
    text = ""
    reader = PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # Prevent NoneType error
            text += page_text + "\n"

    return text.strip()


# -----------------------------
# DOCX EXTRACTOR (SAFE)
# -----------------------------
def extract_docx(file):
    text = ""
    document = docx.Document(file)

    for para in document.paragraphs:
        if para.text:
            text += para.text + "\n"

    return text.strip()
