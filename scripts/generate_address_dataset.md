Getting a dataset of addresses can be challenging as this type of information may not be freely available due to privacy concerns. However, there are several approaches and sources where you can obtain address datasets or create your own:

### 1. **Open Datasets**
   - **OpenStreetMap (OSM)**:
     - **OpenStreetMap** is a well-known open data project that offers geospatial data, including addresses, for many parts of the world. You can extract address data from OSM using APIs or tools like **Overpass API**.
     - [OpenStreetMap](https://www.openstreetmap.org) also offers data exports which can be used for research and analysis.
   - **Geonames**:
     - **Geonames** provides a wide range of geographical data, including cities, zip codes, and addresses. The dataset is open for non-commercial use.
     - You can explore the dataset at [Geonames.org](https://www.geonames.org/).
   - **Kaggle**:
     - **Kaggle** is an excellent source for various types of datasets, including location and address data. You can find datasets that contain addresses, such as housing, restaurant locations, or other geographical data.
     - Search for address datasets at [Kaggle](https://www.kaggle.com/).
   - **Data.gov**:
     - Many countries have open data initiatives that include address-related information, such as the U.S. Government’s [Data.gov](https://www.data.gov/) platform.
   - **Open Data Portals**:
     - Several cities and countries have open data portals where address information is publicly available, such as:
       - [data.gov.uk](https://data.gov.uk/) for the UK.
       - [data.gov.au](https://data.gov.au/) for Australia.

### 2. **Synthetic Dataset Generation**
   - If you can't find a suitable dataset, generating synthetic address data might be an effective approach.
   - **Faker** Library:
     - The **Faker** library in Python can generate synthetic addresses that mimic real-world data. You can generate thousands of addresses for training purposes:
       ```python
       from faker import Faker
       import pandas as pd

       fake = Faker()
       data = []

       for _ in range(1000):
           address = fake.address().replace("\n", ", ")
           data.append({'text': address, 'label': 1})  # Label 1 for address

       df = pd.DataFrame(data)
       df.to_csv('data/address_dataset.csv', index=False)
       ```
     - This approach is particularly useful to quickly generate labeled address data.

### 3. **Scraping Public Sources**
   - **Web Scraping**: 
     - If you need address data, you can scrape addresses from publicly available directories like:
       - **Yellow Pages**: Use tools like **Beautiful Soup** or **Scrapy** to collect business addresses from Yellow Pages directories.
       - **Google Maps** or similar services: You can use APIs to get addresses, though scraping these services without permission is against their terms of service.
   - **Real Estate Websites**:
     - Websites like Zillow or Realtor often provide addresses of listed properties, and you could collect such information through scraping.

### 4. **Use Address APIs**
   - Use APIs that provide address details for educational purposes:
   - **Google Maps API**:
     - Google Maps offers address information, including formatted addresses, via their **Geocoding API**.
     - However, Google Maps is a paid service, and usage must comply with their terms.
   - **HERE API** and **OpenCage Geocoding API**:
     - These services provide address data that can be used for research purposes, although API limits and usage terms apply.

### 5. **Crowdsourced Address Datasets**
   - **Open Address Initiative**:
     - The **Open Addresses** project aims to collect openly licensed address data from around the world.
     - You can check their data collection at [Open Addresses](https://openaddresses.io/).

### 6. **Use Labeled Text Data and Extract Addresses**
   - You can use existing labeled text datasets that contain addresses mixed with other information and manually label them. For example, use datasets related to:
     - **Housing Listings**: These often have detailed addresses.
     - **Restaurant Reviews**: Data from Yelp might contain addresses that are labeled as part of location information.
   - You can create a dataset with mixed examples (addresses and non-addresses) for training.

### Sample Dataset Structure
For training a classification model, you need a dataset where each row has:
- A **text** column with the text block.
- A **label** column indicating whether the text is an address (`1`) or not (`0`).

**Example CSV Data**:
```csv
text,label
"123 Main St, New York, NY 10001, USA",1
"Dear John, I hope you are doing well.",0
"Jl. Sudirman No. 45, Jakarta, Indonesia",1
"Contact our office for further information.",0
```

### Summary
1. **Public Datasets**: Use resources like **OpenStreetMap**, **Geonames**, or open government data.
2. **Generate Synthetic Data**: Use tools like **Faker** to generate addresses.
3. **Web Scraping**: Scrape addresses from public directories.
4. **Address APIs**: Use Google Maps API, HERE API, or OpenCage for data collection.
5. **Mixed Labeled Datasets**: Extract address-like information from existing mixed datasets and label it.

By combining these sources, you can build a comprehensive dataset that can be used to train your model to distinguish address-like text from other types of information effectively.


## FAKER LIBRARY SCRIPT

You can create a script to generate a synthetic dataset using the **Faker** library and save it in your project's `scripts` folder. Here's how you can organize it:


### Script Details:
1. **Imports**:
   - **Faker**: Generates synthetic addresses and random non-address sentences.
   - **Pandas**: Helps create a structured CSV dataset.
   - **os**: Used for creating folders if they do not already exist.

2. **Synthetic Address Generation**:
   - **Faker instance**: Generates realistic addresses (`fake.address()`) and random sentences for non-address examples (`fake.sentence()`).
   - Addresses are labeled as `1` and non-address sentences as `0`.

3. **Saving the Dataset**:
   - The dataset is saved in a CSV format to the `data` folder (`business_card_ocr/data/address_dataset.csv`).
   - The **label** column contains `1` for addresses and `0` for non-address text.

### Step 3: Running the Script
To run the script and generate the dataset, follow these steps:

1. **Navigate to the Root Directory**:
   - Open a terminal and navigate to the project’s root directory (`business_card_ocr`):
     ```bash
     cd business_card_ocr
     ```

2. **Run the Script**:
   - Execute the script to generate the synthetic dataset:
     ```bash
     python scripts/generate_address_dataset.py
     ```

3. **Verify Dataset Generation**:
   - Once the script is done running, you should see `address_dataset.csv` in the `data` folder. It will contain both synthetic addresses and non-address sentences.

### Using the Generated Dataset
After generating the dataset, you can use it for training your machine learning model (`train_address_model.py`). This file (`address_dataset.csv`) will serve as the labeled data to train a classifier capable of determining whether a block of text is an address or not.

Since this project is specifically for business card recognition, it makes more sense to generate non-address examples that reflect the other kinds of information typically found on business cards, such as job titles, company names, emails, and phone numbers. This way, the model can learn to differentiate addresses from other realistic, relevant entities found on business cards.

Suggested Strategy for Non-Address Examples
The goal is to ensure that the model sees realistic data, improving its ability to distinguish between addresses and other entities. Here’s how you can generate the non-address examples more effectively:

Job Titles: Use typical job titles found on business cards.
Company Names: Generate plausible company names.
Emails: Generate email addresses that would commonly be seen on business cards.
Phone Numbers: Generate phone numbers, potentially in different formats (e.g., with and without country codes).

Benefits of This Approach:
Business Context Relevance: The non-address examples are now realistic for a business card context, allowing the classifier to learn to differentiate between addresses and other information commonly present on business cards.
Better Model Training: By providing varied examples, the model will be more adept at recognizing the distinctions between addresses and other business card entities, reducing false positives and false negatives.
