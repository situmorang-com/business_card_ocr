# enhanced_address_extraction.py

import os
import joblib
import pytesseract
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer

# Load the trained model and vectorizer
models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
model_file = os.path.join(models_folder, 'trained_model.pkl')
loaded_model = joblib.load(model_file)

vectorizer_file = os.path.join(models_folder, 'vectorizer.pkl')
vectorizer = joblib.load(vectorizer_file)

# OCR function to extract text from business card images
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to validate addresses from extracted text
def validate_addresses(extracted_text):
    extracted_addresses = [line for line in extracted_text.split('\n') if line.strip()]
    
    # Validate the extracted addresses
    addresses_vectorized = vectorizer.transform(extracted_addresses)
    predictions = loaded_model.predict(addresses_vectorized)
    valid_addresses = [address for address, prediction in zip(extracted_addresses, predictions) if prediction == 1]
    
    return valid_addresses

# Example usage with an OCR-extracted address
ocr_images_folder = os.path.join(os.path.dirname(__file__), '..', 'input')
example_image = os.path.join(ocr_images_folder, 'example_business_card.jpg')

# Extract text and validate addresses from the image
extracted_text = extract_text_from_image(example_image)
valid_addresses = validate_addresses(extracted_text)
for address in valid_addresses:
    print(f'Valid Address: {address}')
