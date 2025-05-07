# job_monitoring_system.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import time

# Scrape job listings from karkidi.com (simplified mock)
def scrape_karkidi_jobs(keyword="data science", pages=1):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://www.karkidi.com/Find-Jobs/{page}/all/India?search={query}"
    jobs_list = []

    for page in range(1, pages + 1):
        url = base_url.format(page=page, query=keyword.replace(' ', '%20'))
        print(f"Scraping page: {page}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        job_blocks = soup.find_all("div", class_="ads-details")
        for job in job_blocks:
            try:
                title = job.find("h4").get_text(strip=True)
                company = job.find("a", href=lambda x: x and "Employer-Profile" in x).get_text(strip=True)
                location = job.find("p").get_text(strip=True)
                experience = job.find("p", class_="emp-exp").get_text(strip=True)
                key_skills_tag = job.find("span", string="Key Skills")
                skills = key_skills_tag.find_next("p").get_text(strip=True) if key_skills_tag else ""
                summary_tag = job.find("span", string="Summary")
                summary = summary_tag.find_next("p").get_text(strip=True) if summary_tag else ""

                jobs_list.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Experience": experience,
                    "Summary": summary,
                    "Skills": skills
                })
            except Exception as e:
                print(f"Error parsing job block: {e}")
                continue

        time.sleep(1)  # Be nice to the server

    return pd.DataFrame(jobs_list)





# Preprocess the 'skills' column
def preprocess_skills(df):
    df['Skills'] = df['Skills'].apply(lambda x: re.sub(r'[^a-zA-Z0-9, ]', '', x).lower())
    return df

# Add this at the top or near other functions
def comma_tokenizer(text):
    return text.split(',')


# Vectorize the skills for clustering
def vectorize_skills(df):
    vectorizer = TfidfVectorizer(tokenizer=comma_tokenizer)
    X = vectorizer.fit_transform(df['Skills'])
    return X, vectorizer

# Load the saved clustering model and vectorizer
def load_model(model_path="job_model.pkl"):
    with open(model_path, 'rb') as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer


# if __name__ == "__main__":
#     df_jobs = scrape_karkidi_jobs(keyword="data science", pages=2)
#     print(df_jobs.head())