

import base64
import io
from PIL import Image
import easyocr
import re

def convert_bytecode_to_image(image_bytecode, output_path="output_image.png"):

    try:
        # Ensure proper padding for Base64 string
        image_bytecodebase = base64.b64decode(image_bytecode)
        image_stream = io.BytesIO(image_bytecodebase)
        image = Image.open(image_stream)
        # Save the image locally

        image.save(output_path, format= "PNG")
        print(f"Image saved successfully at {output_path}")

        return image
    except base64.binascii.Error as e:
        raise ValueError(f"Invalid Base64 input: {e}")
    except IOError as e:
        raise ValueError(f"Error reading image file: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error during image conversion: {e}")


def perform_ocr(image_path):
    
    try:
        reader = easyocr.Reader(['en'])  
        results = reader.readtext(image_path)
        print("OCR Results:", results)  
        return results
    except Exception as e:
        raise ValueError(f"Error performing OCR: {e}")


def extract_document_details(results):
    
    extracted_text = " ".join([text.upper() for (_, text, _) in results])
    print("Extracted Text for Parsing:", extracted_text)

    patterns = {
        "Name": r"\bNAME[:\-]?\s*([A-Z\s]+)",
        "Father's Name": r"\b(FATHER'S NAME|S/O|SLO)\s*[:\-]?\s*([A-Z\s]+)",
        "Date of Birth": r"\b(DOB|DATE OF BIRTH)\s*[:\-]?\s*(\d{2}[-/]\d{2}[-/]\d{4})",
        "PAN Number": r"\b([A-Z]{5}[0-9]{4}[A-Z]{1})\b",
    }

    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, extracted_text)
        if match:
            extracted_data[field] = match.group(1).strip() if field != "Date of Birth" else match.group(2).strip()
        else:
            extracted_data[field] = None

    print("Extracted Data:", extracted_data)  # Log final output
    return extracted_data