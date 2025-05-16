# utils/notify.py
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
import os

def notify_users(matches, preferences_file, notified_jobs_file="notified_jobs.json"):
    # Load user preferences from the JSON file
    with open(preferences_file, 'r') as file:
        user_preferences = json.load(file)

    # Load previously notified jobs
    if not os.path.exists(notified_jobs_file):
        notified_jobs = {}
    else:
        with open(notified_jobs_file, 'r') as file:
            notified_jobs = json.load(file)

    sender_email = "jobmonitor19@gmail.com"  # Replace with your email
    load_dotenv()  # Load environment variables from .env file
    # Use environment variable for the password
    sender_password = os.getenv("GMAIL_APP_PASSWORD")
    


    for user_email, preferences in user_preferences.items():
        if not preferences.get("notify", False):
            continue  # Skip users who have opted out of notifications

        user_cluster = preferences.get("predicted_cluster")
        cluster_matches = matches[matches['cluster'] == user_cluster]

        # Filter out jobs that have already been notified
        new_jobs = cluster_matches[~cluster_matches['id'].isin(notified_jobs.get(user_email, []))]

        if new_jobs.empty:
            print(f"No new jobs available for {user_email} in Cluster {user_cluster}.")
            continue

        subject = "New Job Matches Based on Your Preferences"
        body = f"Here are the new jobs matching your interests in Cluster {user_cluster}:\n\n"

        for _, row in new_jobs.iterrows():
            body += f"- {row['title']} at {row['company']}\n  Skills: {row['skills']}\n\n"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent to {user_email}")

            # Update notified jobs
            notified_jobs.setdefault(user_email, []).extend(new_jobs['id'].tolist())
        except Exception as e:
            print(f"❌ Failed to send email to {user_email}: {e}")

    # Save updated notified jobs
    with open(notified_jobs_file, 'w') as file:
        json.dump(notified_jobs, file, indent=4)



