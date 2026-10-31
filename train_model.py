
import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


# Load the datasets
fake = pd.read_csv("dataset/Fake.csv")
real = pd.read_csv("dataset/True.csv")

# Add labels
fake["label"] = 0
real["label"] = 1

# Combine both datasets
data = pd.concat([fake, real], ignore_index=True)

# Combine title and text
data["content"] = data["title"].fillna("") + " " + data["text"].fillna("")

# Remove empty news
data = data[data["content"].str.strip() != ""]

# Prepare input and output
X = data["content"]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create machine learning model
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000)),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train the model
model.fit(X_train, y_train)

# Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model training completed!")
print("Accuracy:", accuracy * 100, "%")

# Create model folder
os.makedirs("model", exist_ok=True)

# Save trained model
with open("model/fake_news_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")
