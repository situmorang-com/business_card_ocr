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