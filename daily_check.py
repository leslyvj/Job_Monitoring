# daily_check.py

import os
import json
import pickle
from utils.notify import notify_users
from job_monitoring_system import scrape_karkidi_jobs, preprocess_skills, load_model

# Load previous jobs
def load_seen_jobs(filename="seen_jobs.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_jobs(jobs, filename="seen_jobs.json"):
    with open(filename, 'w') as f:
        json.dump(list(jobs), f, indent=4)

# Load user preferences
def load_user_preferences(filename="user_preferences.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}


# Main process
def check_new_jobs():
    seen_jobs = load_seen_jobs()
    prefs = load_user_preferences()
    df = scrape_karkidi_jobs(keyword="data science", pages=6)
    df = preprocess_skills(df)

    model, vectorizer = load_model()
    X = vectorizer.transform(df['Skills'])
    df['cluster'] = model.predict(X)

    # Make sure 'id', 'title', 'company', 'skills' columns exist for notify_users
    if 'id' not in df.columns:
        df['id'] = df['Title'] + ' - ' + df['Company']
    if 'title' not in df.columns:
        df['title'] = df['Title']
    if 'company' not in df.columns:
        df['company'] = df['Company']
    if 'skills' not in df.columns:
        df['skills'] = df['Skills']

    # Call notify_users with the DataFrame and preferences file
    notify_users(df, "user_preferences.json")

    # Optionally update seen jobs if needed
    new_seen = set(df['id'])
    save_seen_jobs(new_seen)

check_new_jobs()
