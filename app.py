# app.py (Flask Web App Version of Job Monitoring System with Email-only Login and Notification Option)

from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import os
import json
import pickle
from job_monitoring_system import scrape_karkidi_jobs, preprocess_skills, load_model, vectorize_skills

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Load or create user preferences
def load_user_preferences(filename="user_preferences.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_user_preferences(prefs, filename="user_preferences.json"):
    with open(filename, 'w') as f:
        json.dump(prefs, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html', user=session.get('email'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        cluster = int(request.form['cluster'])
        notify = 'notify' in request.form

        prefs = load_user_preferences()
        prefs[email] = {"preferred_cluster": cluster, "notify": notify}
        save_user_preferences(prefs)

        session['email'] = email
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/jobs')
def jobs():
    if 'email' not in session:
        return redirect(url_for('login'))

    df = scrape_karkidi_jobs()
    df = preprocess_skills(df)

    if not os.path.exists("job_model.pkl"):
        X, vectorizer = vectorize_skills(df)
        from sklearn.cluster import KMeans
        model = KMeans(n_clusters=5, random_state=42)
        df['cluster'] = model.fit_predict(X)
        with open("job_model.pkl", 'wb') as f:
            pickle.dump((model, vectorizer), f)
    else:
        model, vectorizer = load_model()
        X = vectorizer.transform(df['Skills'])
        df['cluster'] = model.predict(X)

    cluster_filter = request.args.get('cluster')
    if cluster_filter is not None:
        df = df[df['cluster'] == int(cluster_filter)]

    return render_template('jobs.html', tables=[df.to_html(classes='data', header="true")], cluster_filter=cluster_filter, user=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)
