from pdfminer.high_level import extract_text as pdf_extract_text
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import io
from pdf2image import convert_from_path
import logging

def extract_text_from_pdf(pdf_path, dpi=300, tesseract_config=None, enhance=False):
    try:
        text = pdf_extract_text(pdf_path)
        if text and len(text.strip()) > 50:
            return text
        logging.info("Minimal text detected. Using OCR.")
    except Exception as e:
        logging.warning(f"Direct text extraction failed: {e}. Attempting OCR...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        all_text = []
        for i, image in enumerate(images):
            if enhance:
                image = _preprocess_image(image)
            page_text = pytesseract.image_to_string(image, config=tesseract_config) if tesseract_config else pytesseract.image_to_string(image)
            if page_text.strip():
                all_text.append(f"--- Page {i+1} ---\n{page_text}")
        combined_text = "\n\n".join(all_text)
        if combined_text.strip():
            logging.info(f"Extracted text from {len(images)} page(s) via OCR")
            return combined_text
        else:
            return "Could not extract text from the PDF. Ensure the document is clear and readable."
    except Exception as e:
        return f"OCR extraction failed: {e}. Ensure pdf2image dependencies are installed."

def extract_text_from_image(image_file, tesseract_config=None, enhance=False):
    image = Image.open(image_file)
    if enhance:
        image = _preprocess_image(image)
    return pytesseract.image_to_string(image, config=tesseract_config) if tesseract_config else pytesseract.image_to_string(image)

def _preprocess_image(image):
    img = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    return img
