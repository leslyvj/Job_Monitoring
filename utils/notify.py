# utils/notify.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def notify_via_email(matches, user_email):
    sender_email = "your-email@gmail.com"  # Replace with your email
    sender_password = "your-password"      # Replace with your email password or app password

    subject = "New Job Matches Based on Your Preferences"
    body = "Here are the new jobs matching your interests:\n\n"

    for _, row in matches.iterrows():
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
