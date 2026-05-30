import pdfplumber
import pytesseract
from PIL import Image

# Tesseract path (VERY IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(file):
    text = ""

    # ===== NORMAL EXTRACTION =====
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # ===== OCR FALLBACK =====
    if not text.strip():
        file.seek(0)

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                image = page.to_image(resolution=300)
                pil_image = image.original

                ocr_text = pytesseract.image_to_string(pil_image)
                text += ocr_text

    return text