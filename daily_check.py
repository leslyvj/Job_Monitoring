# daily_check.py

import os
import json
import pickle
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

# Mock notification
def notify_user(email, job):
    print(f"\n📬 Notifying {email}: New job posted that matches your interest!")
    print(f"→ {job['Title']} at {job['Company']} | Location: {job['Location']}")

# Main process
def check_new_jobs():
    seen_jobs = load_seen_jobs()
    prefs = load_user_preferences()
    df = scrape_karkidi_jobs(keyword="data science", pages=3)
    df = preprocess_skills(df)

    model, vectorizer = load_model()
    X = vectorizer.transform(df['Skills'])
    df['cluster'] = model.predict(X)

    new_seen = seen_jobs.copy()

    for _, job in df.iterrows():
        job_id = job['Title'] + ' - ' + job['Company']
        if job_id not in seen_jobs:
            for email, pref in prefs.items():
                if pref.get("notify") and job['cluster'] == pref.get("preferred_cluster"):
                    notify_user(email, job)
            new_seen.add(job_id)

    save_seen_jobs(new_seen)

if __name__ == "__main__":
    check_new_jobs()
