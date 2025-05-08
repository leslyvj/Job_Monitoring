# utils/notify.py
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def notify_users(matches, preferences_file):
    # Load user preferences from the JSON file
    with open(preferences_file, 'r') as file:
        user_preferences = json.load(file)

    sender_email = "jobmonitor19@gmail.com"  # Replace with your email
    sender_password = "12345678a,"      # Replace with your email password or app password

    for user_email, preferences in user_preferences.items():
        if not preferences.get("notify", False):
            continue  # Skip users who have opted out of notifications

        user_cluster = preferences.get("preferred_cluster")
        cluster_matches = matches[matches['cluster'] == user_cluster]

        if cluster_matches.empty:
            print(f"No new jobs available for {user_email} in Cluster {user_cluster}.")
            continue

        subject = "New Job Matches Based on Your Preferences"
        body = f"Here are the new jobs matching your interests in Cluster {user_cluster}:\n\n"

        for _, row in cluster_matches.iterrows():
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
        except Exception as e:
            print(f"❌ Failed to send email to {user_email}: {e}")



# Example usage
matches = pd.DataFrame([
    {'title': 'Software Engineer', 'company': 'TechCorp', 'skills': 'Python, Django', 'cluster': 1},
    {'title': 'Data Scientist', 'company': 'DataInc', 'skills': 'Python, Machine Learning', 'cluster': 2},
])

preferences_file = "d:\\job_monitoring_system\\user_preferences.json"
notify_users(matches, preferences_file)