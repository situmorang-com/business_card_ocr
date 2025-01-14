import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# Load the address dataset
input_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
address_file = os.path.join(input_folder, 'address_dataset.csv')

# Save the models in the models folder
models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')


# Load the processed data into a DataFrame
df = pd.read_csv(address_file)

# Preprocess the data
df['text'] = df['text'].str.replace(r'"', '')
df['text'] = df['text'].str.replace(r', 1', '')

# Vectorize the text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])


# Save the vectorizer
os.makedirs(models_folder, exist_ok=True)
vectorizer_file = os.path.join(models_folder, 'vectorizer.pkl')
joblib.dump(vectorizer, vectorizer_file)

# Use the label column for target values
y = df['label']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Train a logistic regression model with class weights balanced
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

# Save the trained model
os.makedirs(models_folder, exist_ok=True)
model_file = os.path.join(models_folder, 'trained_model.pkl')
joblib.dump(model, model_file)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred, zero_division=1))
