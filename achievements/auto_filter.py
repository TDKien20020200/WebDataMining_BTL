# Vấn đề 3: Tự động hóa phân loại ngành nghề
# Thách thức: Các công việc có thể thuộc nhiều ngành nghề, nhưng việc phân loại thủ công tốn nhiều thời gian và dễ xảy ra sai sót.
# Giải pháp: Sử dụng mô hình học máy (như Naïve Bayes hoặc Transformer) để tự động phân loại các công việc dựa trên nội dung mô tả.
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load data
data = pd.read_json('./files/myamcat.json')

# Prepare data
data = data.dropna(subset=['jd', 'classification'])
X = data['jd']
y = data['classification']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model
import joblib
joblib.dump(pipeline, 'job_classifier.pkl')
print("Model saved as 'job_classifier.pkl'")
