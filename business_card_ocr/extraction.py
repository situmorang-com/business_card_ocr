import pytesseract
import re
import cv2
import numpy as np
import spacy

# Load spaCy model for better entity recognition
nlp = spacy.load("en_core_web_sm")

def extract_text(image):
    return pytesseract.image_to_string(image)

def detect_text_regions(image_path):
    # Load the pre-trained EAST model for text detection
    net = cv2.dnn.readNet("models/frozen_east_text_detection.pb")
    image = cv2.imread(image_path)
    orig = image.copy()
    (H, W) = image.shape[:2]

    # Ensure the image dimensions are divisible by 32
    new_W = (W // 32) * 32
    new_H = (H // 32) * 32
    resized_image = cv2.resize(image, (new_W, new_H))
    (H, W) = resized_image.shape[:2]

    # Define the two output layers we need from the EAST model
    layer_names = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"
    ]

    # Prepare the image for input to the network
    blob = cv2.dnn.blobFromImage(resized_image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layer_names)

    # Decode the predictions and apply non-maxima suppression
    rectangles = []
    confidences = []

    # Loop through rows and columns to extract bounding boxes and confidences
    for y in range(0, geometry.shape[2]):
        for x in range(0, geometry.shape[3]):
            score = scores[0, 0, y, x]
            if score > 0.5:
                offset_x, offset_y = (x * 4.0, y * 4.0)
                angle = geometry[0, 4, y, x]
                h = geometry[0, 0, y, x]
                w = geometry[0, 1, y, x]

                cos_a = np.cos(angle)
                sin_a = np.sin(angle)

                end_x = int(offset_x + (cos_a * w) + (sin_a * h))
                end_y = int(offset_y + (sin_a * w) + (cos_a * h))

                rectangles.append((end_x, end_y))

    return rectangles

def parse_contact_details(text):
    # Extract email using regex
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email = re.findall(email_pattern, text)

    # Extract phone number using regex
    phone_pattern = r'\+?\d[\d -]{8,}\d'
    phone = re.findall(phone_pattern, text)

    # Extract address lines that contain keywords like 'Floor', 'Jl', 'Jalan', or 'Kav'
    lines = text.split('\n')
    address_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Check if the line contains any address-related keyword
        if any(keyword in line.lower() for keyword in ["floor", "jl", "jalan", "kav"]):
            address_lines.append(line)
            # Check the next few lines for city names, zip codes, or country names
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # Stop if the line contains phone number indicators or is unrelated
                if re.search(r'\b(tel|mobile|fax)\b', next_line.lower()) or re.search(phone_pattern, next_line):
                    break
                # Continue adding if the line contains address-related elements
                if re.search(r'\b\d{4,}\b', next_line) or any(keyword in next_line.lower() for keyword in ["indonesia", "jakarta", "selatan", "utara", "timur", "barat"]):
                    address_lines.append(next_line)
                    j += 1
                else:
                    break
            i = j - 1  # Skip over the lines already added
        i += 1

    address = ", ".join(address_lines) if address_lines else "Not found"

    # Define a list of words related to geography or common address elements
    geography_keywords = [
        "jakarta", "indonesia", "selatan", "utara", "timur", "barat", "tengah",
        "rt", "rw", "kav", "jalan", "jl", "floor", "zip", "kode pos"
    ]

    # Use spaCy to analyze the text and find named entities
    doc = nlp(text)
    name = "Unknown"
    company = "Unknown"
   
    # Job titles to help locate names
    job_titles = ["head", "manager", "director", "ceo", "cto", "founder", "president", "lead", "officer", "specialist"]

    # Split the text by lines for manual processing
    lines = text.split('\n')

    # Attempt to find the name based on its position above the job title
    for i, line in enumerate(lines):
        lower_line = line.lower().strip()
        if any(title in lower_line for title in job_titles):
            # The line above this one could be the name
            if i > 0:
                potential_name = lines[i - 1].strip()
                if potential_name and not any(keyword in potential_name.lower() for keyword in ["floor", "jl", "jalan", "kav"] + geography_keywords):
                    name = potential_name
                    break

    # If no name was found, fall back to using spaCy entity detection
    if name == "Unknown":
        for ent in doc.ents:
            if ent.label_ == "PERSON" and name == "Unknown":
                # Ensure the detected name doesn't contain address-related keywords or geographic locations
                if not any(keyword in ent.text.lower() for keyword in geography_keywords):
                    name = ent.text
            elif ent.label_ == "ORG" and company == "Unknown":
                company = ent.text

    # Further refine name extraction by ensuring the detected name is not likely a company name
    if "PT " in name or "Ltd" in name or "Inc" in name:
        name = "Unknown"

    return {
        'Name': name.strip(),
        'Email': email[0] if email else "Not found",
        'Phone': phone[0] if phone else "Not found",
        'Company': company.strip(),
        'Address': address
    }
