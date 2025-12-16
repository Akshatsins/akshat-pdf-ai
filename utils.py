import pytesseract
from pdf2image import convert_from_bytes



def extract_text_from_pdf(file_bytes):
    """
    1. Converts a PDF file (bytes) into images.
    2. Uses Tesseract to read text from those images.
    """
    try:
        
        images = convert_from_bytes(file_bytes)
        
        full_text = ""
        
        
        for i, img in enumerate(images):
            page_text = pytesseract.image_to_string(img)
            full_text += f"--- Page {i+1} ---\n{page_text}\n"
            
        return full_text
    except Exception as e:
        return f"Error processing PDF: {e}"