#!/usr/bin/env python3

import os
import time
import sqlite3
import psutil
import logging
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

#############################
#  Load Environment (.env)  #
#############################
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
DB_NAME = os.getenv("DB_NAME", "monitor_system.db")
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80"))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))

########################
# Logging Configuration
########################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("monitor.log", mode="a")
    ]
)

########################
# Globals
########################
LAST_EMAIL_TIME = 0.0  # tracks last email sent time (for cooldown)
COOLDOWN_SECONDS = 60  # e.g., 60 seconds spam-prevention

########################
# Database Functions
########################
def create_db():
    """
    Creates the SQLite database and metrics table if not found.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                ram_usage REAL
            )
        ''')
        conn.commit()
        logging.info(f"Database {DB_NAME} created/verified successfully.")
    except Exception as e:
        logging.error(f"Error creating/verifying DB: {e}")
    finally:
        conn.close()

def insert_metrics(cpu_usage, ram_usage):
    """
    Inserts a record of CPU and RAM usage into the DB.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO metrics (cpu_usage, ram_usage)
            VALUES (?, ?)
        ''', (cpu_usage, ram_usage))
        conn.commit()
    except Exception as e:
        logging.error(f"Error inserting metrics: {e}")
    finally:
        conn.close()

########################
# Metric Collection
########################
def collect_metrics():
    """
    Collect CPU and RAM usage using psutil.
    Returns (cpu_usage, ram_usage).
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    ram_usage = ram_info.percent
    return cpu_usage, ram_usage

########################
# Email Sending
########################
def send_email(subject, body):
    """
    Sends an email alert via Gmail SMTP using credentials from .env.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def send_email_with_cooldown(subject, body, cooldown=COOLDOWN_SECONDS):
    """
    Sends an email if cooldown has elapsed.
    Prevents spam if CPU remains above threshold for extended periods.
    """
    global LAST_EMAIL_TIME
    now = time.time()

    if (now - LAST_EMAIL_TIME) < cooldown:
        logging.info("Cooldown active; skipping email alert.")
        return

    LAST_EMAIL_TIME = now  # update the last email time
    send_email(subject, body)

########################
# Main Loop
########################
def main():
    # Sanity checks for env variables
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        logging.error("Missing email credentials in .env!")
        return

    create_db()

    while True:
        cpu_val, ram_val = collect_metrics()
        insert_metrics(cpu_val, ram_val)
        logging.info(f"CPU: {cpu_val:.1f}% | RAM: {ram_val:.1f}%")

        if cpu_val > CPU_THRESHOLD:
            subject = "CPU HIGH ALERT"
            body = f"CPU usage is {cpu_val:.1f}%, exceeding threshold {CPU_THRESHOLD}%."
            send_email_with_cooldown(subject, body, cooldown=COOLDOWN_SECONDS)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
