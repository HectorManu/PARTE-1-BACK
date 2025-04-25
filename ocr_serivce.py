import pytesseract
from PIL import Image
import os
import re

def process_image(image_path):
    """
    Procesa una imagen usando Tesseract OCR y devuelve el texto extraído
    """
    try:
        # Abrir la imagen con PIL
        image = Image.open(image_path)
        
        # Extraer texto usando pytesseract
        text = pytesseract.image_to_string(image, lang='spa')
        
        # Limpiar y normalizar el texto
        text = clean_text(text)
        
        return text
    except Exception as e:
        print(f"Error al procesar imagen: {str(e)}")
        raise

def clean_text(text):
    """
    Limpia y normaliza el texto extraído del OCR
    """
    if not text:
        return ""
    
    # Eliminar caracteres no deseados
    text = re.sub(r'[^\w\s.,:/€$%]', '', text)
    
    # Eliminar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar líneas vacías
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = '\n'.join(lines)
    
    return text
