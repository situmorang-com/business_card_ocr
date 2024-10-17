import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Step 1: Load your dataset
# Assume we have a dataset with columns 'text' and 'label' (1 for address, 0 for non-address)
data = pd.read_csv('address_dataset.csv')

# Step 2: Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# Step 3: Preprocessing and Vectorization using TF-IDF
tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)

# Step 4: Define the model - Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Step 5: Create a pipeline that includes the vectorizer and classifier
pipeline = Pipeline([
    ('tfidf', tfidf),
    ('classifier', rf_model)
])

# Step 6: Train the model
pipeline.fit(X_train, y_train)

# Step 7: Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Step 8: Evaluate the model
print(classification_report(y_test, y_pred))

# Step 9: Using the model for new predictions
new_texts = ["123 Main Street, New York, NY", "Dear Mr. Smith, I hope you are doing well."]
predictions = pipeline.predict(new_texts)
print(predictions)
