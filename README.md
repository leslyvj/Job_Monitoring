---
# Job Monitoring System
---
## Overview

The **Job Monitoring System** is a job alert web application that scrapes listings from [Karkidi.com](https://karkidi.com/), classifies them using unsupervised machine learning, and notifies users via email based on their skill preferences.

Users can:

* Register using their **Gmail** address.
* Enter their **skills**.
* Select the **notification option** to receive job alerts.
* Get automatically **clustered** into a suitable category based on skills.
* Receive **email notifications** about new relevant jobs.

## Features

* **Skill-based clustering** using KMeans algorithm.
* **Daily job scraping and classification**.
* **Email alerts** using Gmail App Passwords.
* **Task Scheduler**-based automation for daily execution.
* **User preferences and job tracking** saved in `.json` files.

---

## File Structure

```
job_monitoring_system/
│
├── templates/
│   ├── index.html
│   ├── jobs.html
│   ├── login.html
│   └── register.html
│
├── utils/
│   └── notify.py
│
├── __pycache__/
├── .gitignore
├── app.py                  # Flask web app
├── daily_check.py          # Daily script for checking new jobs
├── job_model.pkl           # Trained clustering model
├── job_monitoring_system.py # Core job scraping & prediction logic
├── notified_jobs.json      # Tracks which jobs have been notified
├── requirements.txt        # Python dependencies
├── seen_jobs.json          # Tracks previously seen jobs
├── train_model.py          # Scrapes and trains the model
└── user_preferences.json   # Stores user registration & preferences
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd job_monitoring_system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Gmail Configuration

To send emails securely, you must generate an app password for your Gmail account:

* Enable 2-Step Verification in your Google Account.

* Navigate to App Passwords.

* Generate an app password for "Mail".

* Use this password in your script for authentication.

You can optionally store credentials in a .env file and load them using python-dotenv.

### 4. Train the Model

Before using the system, run:

```bash
python train_model.py
```

This will:

* Scrape job data from Karkidi.com.
* Vectorize the job skills.
* Apply KMeans clustering.
* Save the model as `job_model.pkl`.

### 5. Run the Web App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Daily Automation with Task Scheduler (Windows)

To automatically check for new jobs and send notifications:

1. Open **Task Scheduler**.
2. Create a new **Basic Task** named `Job Notifier`.
3. Trigger: **Daily**.
4. Action: **Start a program**.
5. **Program/script**:

   ```
   C:\Users\shamm\AppData\Local\Programs\Python\Python312\python.exe
   ```
6. **Add arguments**:

   ```
   daily_check.py
   ```
7. **Start in**:

   ```
   D:\job_monitoring_system
   ```
8. Save the task.

> This will run `daily_check.py` daily to check for new jobs and notify users.

---

## Key Files

| File                       | Description                           |
| -------------------------- | ------------------------------------- |
| `app.py`                   | Flask server and routes               |
| `train_model.py`           | Trains the job clustering model       |
| `job_monitoring_system.py` | Main scraping and prediction logic    |
| `daily_check.py`           | Executes scraping + notification      |
| `notify.py`                | Sends email notifications             |
| `job_model.pkl`            | Trained clustering model              |
| `user_preferences.json`    | Registered users and their skills     |
| `notified_jobs.json`       | Tracks jobs already sent via mail     |
| `seen_jobs.json`           | Stores all seen jobs to avoid repeats |

---

## Notes

* Ensure your Gmail App Password is valid and up-to-date in `notify.py`.
* Each user is automatically assigned a **cluster** based on their skill input.
* You can reset the system by clearing `.json` files if needed (e.g. `notified_jobs.json`).

---

## License

MIT License

---

