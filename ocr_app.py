import os
import cv2
import pytesseract
import re
from PIL import Image
import pyheif

def convert_heic_to_jpeg(heic_path, jpeg_path):
    # Load HEIC image using pyheif
    heif_file = pyheif.read(heic_path)

    # Convert the HEIC to a Pillow Image
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data, 
        "raw", 
        heif_file.mode, 
        heif_file.stride
    )

    # Save the image as JPEG with reduced quality to make it smaller
    image.save(jpeg_path, "JPEG", quality=70)

def preprocess_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to make the text more visible
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return binary_image

def extract_text(image):
    return pytesseract.image_to_string(image)

def parse_contact_details(text):
    # Extract email using regex
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email = re.findall(email_pattern, text)

    # Extract phone number using regex
    phone_pattern = r'\+?\d[\d -]{8,}\d'
    phone = re.findall(phone_pattern, text)

    # Extract name (simple approach: assuming first line contains the name)
    lines = text.split('\n')
    name = lines[0] if lines else "Unknown"

    return {
        'Name': name.strip(),
        'Email': email[0] if email else "Not found",
        'Phone': phone[0] if phone else "Not found"
    }

def main():
    input_folder = "input"
    output_folder = "cards"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all HEIC files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(input_folder, filename)
            jpeg_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")
            convert_heic_to_jpeg(heic_path, jpeg_path)
            print(f"Converted {filename} to JPEG and saved to {jpeg_path}")

    print("All HEIC files have been converted to JPEG.")

if __name__ == "__main__":
    main()
