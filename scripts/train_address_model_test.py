import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load the address dataset
input_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
address_file = os.path.join(input_folder, 'address_dataset.csv')

# Load the processed data into a DataFrame
df = pd.read_csv(address_file)

# Preprocess the data
df['text'] = df['text'].str.replace(r'"', '')
df['text'] = df['text'].str.replace(r', 1', '')

# Vectorize the text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])

# Use the label column for target values
y = df['label']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model
models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(models_folder, exist_ok=True)
model_file = os.path.join(models_folder, 'trained_model.pkl')
joblib.dump(model, model_file)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Load the trained model for use in the business card OCR
loaded_model = joblib.load(model_file)

# Example function to predict if extracted addresses are valid or not
def predict_address(addresses):
    # Vectorize the addresses using the same vectorizer used during training
    addresses_vectorized = vectorizer.transform(addresses)
    predictions = loaded_model.predict(addresses_vectorized)
    return predictions

# Example usage with extracted addresses from OCR
extracted_addresses = [
    "Jl. Raya Pos Pengumben No. 11",
    "Jl. Letjen S. Parman Kav. 21",
    "Central Park, Jl. Letjen. S. Parman",
    "Edmund Situmorang"
]

predictions = predict_address(extracted_addresses)
for address, prediction in zip(extracted_addresses, predictions):
    validity = 'Valid' if prediction == 1 else 'Invalid'
    print(f'Address: {address} - {validity}')
