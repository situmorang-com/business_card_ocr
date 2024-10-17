# Step 1: Install Poetry
# Install Poetry using the following command
curl -sSL https://install.python-poetry.org | python3 -

# Step 2: Create a New Project
# Create a new Poetry project for the business card OCR app
poetry new business_card_ocr
cd business_card_ocr

# Step 3: Add Dependencies
# Add dependencies like Pytesseract, OpenCV, and Pillow
poetry add pytesseract opencv-python Pillow

# Optionally, add development dependencies like pytest
poetry add --dev pytest

# Step 4: Activate the Virtual Environment
# Activate the Poetry environment
poetry shell

# Step 5: Create the Application Script
# Create a Python script named ocr_app.py inside the project directory
touch business_card_ocr/ocr_app.py

# Step 6: Running the Application
# Use Poetry to run your script
poetry run python business_card_ocr/ocr_app.py

# Step 7: Locking Dependencies
# Poetry will automatically create a poetry.lock file to lock the versions of dependencies for reproducibility

# Step 8: Adding Scripts to pyproject.toml (Optional)
# You can add custom scripts to pyproject.toml for convenience
[tool.poetry.scripts]
run-ocr = "business_card_ocr.ocr_app:main"

# Run using custom script
poetry run run-ocr


Identifying the different elements on a business card can be a complex task due to variations in design, fonts, colors, and the layout used by different business cards. Below are some strategies that can help to accurately identify and extract elements such as names, phone numbers, email addresses, job titles, and company names:

### 1. **Optical Character Recognition (OCR) and Preprocessing**
   - **OCR (Pytesseract)**: Use an OCR tool like **Pytesseract** to extract all visible text.
   - **Image Preprocessing**: Improve OCR accuracy with preprocessing techniques such as:
     - **Grayscale Conversion**: Convert the image to grayscale.
     - **Thresholding**: Use adaptive or Otsu’s thresholding to enhance text visibility.
     - **Denoising**: Use filters to reduce image noise.
     - **Morphological Transformations**: Erode or dilate text regions to make the separation of elements more distinct.

### 2. **Text Layout Analysis**
   - **Segmentation**: Use segmentation techniques (e.g., OpenCV **contour detection**) to locate text regions and separate different blocks (name, email, company logo, etc.).
   - **Tesseract OCR Layout Mode**: Use different layout analysis modes provided by Tesseract (such as `--psm` option) to specify how the text is arranged, which can be helpful in better recognizing multi-block text like addresses or names.
     - Example: `--psm 6` can be used for a block of text, while `--psm 3` works well for fully automatic page segmentation.

### 3. **Regular Expressions (Regex) for Key Elements**
   - **Emails**: Use regex to identify email addresses.
     - Pattern: `[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+`
   - **Phone Numbers**: Extract phone numbers by identifying typical formats (country code, separators like `-`, spaces).
     - Pattern: `\+?\d[\d -]{8,}\d`
   - **Website URLs**: Use regex to detect website links.
     - Pattern: `https?://(?:www\.)?[a-zA-Z0-9./-]+`
   - **Addresses**: Look for keywords like "Street," "St.", "Ave," or numeric patterns that suggest addresses.
   - **Names**: Assume names are usually at the top and contain alphabetic characters without symbols.

### 4. **Entity Classification and Machine Learning Models**
   - **Named Entity Recognition (NER)**: Use **NER models** (like those in **spaCy** or **Hugging Face Transformers**) to classify different pieces of text into categories such as name, company, title, etc.
     - Train a model specifically on business card data to improve accuracy.
   - **Heuristics and Keyword Matching**:
     - **Position-Based Extraction**: Often, names are at the top, job titles are right below the name, and contact details (phone, email) are towards the bottom.
     - **Keywords**: Identify common keywords, such as "Tel" or "Phone" for phone numbers, or job titles like "Manager," "Director," etc.

### 5. **Using Template Matching**
   - If you have business cards with similar structures (e.g., for a specific company), you can use **template matching** to identify different fields based on their relative positions.

### 6. **Deep Learning for Image Segmentation**
   - Use **Convolutional Neural Networks (CNNs)** for image segmentation to detect and extract regions of interest (like logos, names, contact details).
   - Pre-trained models like **EAST Text Detector** can be used to detect text regions before passing them to Tesseract for OCR.

### 7. **Post-Processing to Enhance Accuracy**
   - **Remove False Positives**: After extraction, use dictionaries or predefined rules to remove non-sensical data (e.g., check if email includes valid domain extensions).
   - **Confidence Scores**: Use the confidence scores provided by Tesseract to determine if a text block is reliable or needs further analysis.

### **Recommended Strategy for Your App**
1. **Image Preprocessing**: Enhance the image using OpenCV to make the text stand out.
2. **Text Extraction Using OCR**: Extract the text using **Pytesseract**.
3. **Element Identification**:
   - Use **Regex** for structured elements (phone numbers, emails, websites).
   - Use **Keyword Matching** and **Position Analysis** for determining names, job titles, and addresses.
   - Consider integrating **spaCy** for NER to better classify text elements.
4. **Iterative Refinement**: Manually validate a set of business cards to refine your extraction rules and improve your accuracy over time.

If you'd like, I can help you integrate these strategies into your current project. Let me know if you'd like me to add any specific functionality!

business_card_ocr/:
	•	This is the main package of your project containing the application code.
	•	ocr_app.py: The main script to run the OCR process.
	•	preprocessing.py: Contains preprocessing-related functions, such as image enhancement and HEIC-to-JPEG conversion.
	•	extraction.py: Contains functions for text extraction, parsing contact details, etc.
	•	utils.py: Utility functions for file handling, logging, etc.
models/:
	•	Store the pre-trained EAST text detection model and any other machine learning models you might use.
input/:
	•	This folder contains all input images (e.g., HEIC files) that need to be processed.
cards/:
	•	This folder contains the converted JPEG images from the input folder and the processed output images.
tests/:
	•	Contains unit tests to ensure your code works as expected.
	•	test_preprocessing.py and test_extraction.py can contain test cases for validating preprocessing and text extraction functions, respectively.
pyproject.toml:
	•	Poetry configuration file that contains project metadata, dependencies, and other settings.
poetry.lock:
	•	Stores the locked versions of the dependencies to ensure reproducibility.
README.md:
	•	Documentation file that describes the project, how to set it up, and how to run it.
