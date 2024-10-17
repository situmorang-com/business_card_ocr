from faker import Faker
import pandas as pd
import os

# Create a Faker instance
fake = Faker()

# Number of address samples to generate
NUM_SAMPLES = 1000

# Create a list to store generated data
data = []

# Generate synthetic address data
for _ in range(NUM_SAMPLES):
    address = fake.address().replace("\n", ", ")
    data.append({'text': address, 'label': 1})  # Label 1 for address

# Generate non-address examples relevant to business cards
non_address_examples = []

# Generate job titles
for _ in range(NUM_SAMPLES // 4):
    job_title = fake.job()
    non_address_examples.append({'text': job_title, 'label': 0})

# Generate company names
for _ in range(NUM_SAMPLES // 4):
    company_name = fake.company()
    non_address_examples.append({'text': company_name, 'label': 0})

# Generate emails
for _ in range(NUM_SAMPLES // 4):
    email = fake.email()
    non_address_examples.append({'text': email, 'label': 0})

# Generate phone numbers
for _ in range(NUM_SAMPLES // 4):
    phone_number = fake.phone_number()
    non_address_examples.append({'text': phone_number, 'label': 0})

# Combine the address and non-address examples
data.extend(non_address_examples)

# Create a DataFrame
df = pd.DataFrame(data)

# Create the data folder if it doesn't exist
output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

# Save to CSV file
output_path = os.path.join(output_dir, 'address_dataset.csv')
df.to_csv(output_path, index=False)

print(f"Dataset generated and saved to {output_path}")
