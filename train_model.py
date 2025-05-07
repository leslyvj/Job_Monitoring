# train_model.py

import pickle
from sklearn.cluster import KMeans
from job_monitoring_system import scrape_karkidi_jobs, preprocess_skills, vectorize_skills

# Step 1: Scrape and preprocess job data
df = scrape_karkidi_jobs(keyword="data science", pages=2)
df = preprocess_skills(df)

# Step 2: Vectorize skills
X, vectorizer = vectorize_skills(df)

# Step 3: Train clustering model
model = KMeans(n_clusters=5, random_state=42)
model.fit(X)

# Step 4: Save model and vectorizer
with open("job_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model trained and saved to job_model.pkl")
