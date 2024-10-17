import os
from business_card_ocr.preprocessing import convert_heic_to_jpeg, preprocess_image
from business_card_ocr.extraction import detect_text_regions, extract_text, parse_contact_details
from business_card_ocr.utils import create_output_folder

def main():
    input_folder = "input"
    output_folder = "cards"

    # Create output folder if it doesn't exist
    create_output_folder(output_folder)

    # Loop through all HEIC files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(input_folder, filename)
            jpeg_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")
            convert_heic_to_jpeg(heic_path, jpeg_path)
            os.remove(heic_path)
            print(f"Converted {filename} to JPEG, saved to {jpeg_path}, and deleted the original HEIC file.")

    # Loop through all JPEG files in the output folder
    for filename in os.listdir(output_folder):
        if filename.lower().endswith(".jpg"):
            jpeg_path = os.path.join(output_folder, filename)

            # Preprocess image and extract text regions
            rectangles = detect_text_regions(jpeg_path)
            # print(f"Detected text regions in {filename}: {rectangles}")

            # Preprocess image
            preprocessed_image = preprocess_image(jpeg_path)

            # Extract text
            extracted_text = extract_text(preprocessed_image)

            # Parse contact details
            contact_details = parse_contact_details(extracted_text)

            # Display the extracted information
            print("Extracted Contact Details:")
            for key, value in contact_details.items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()