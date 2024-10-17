import os
import pyheif
from PIL import Image
import cv2

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