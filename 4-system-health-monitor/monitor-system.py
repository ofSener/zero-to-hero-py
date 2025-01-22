#modules

import time #for time-related functions
import psutil #for monitoring system resources
import sqlite3 #for storing data
import smtplib #for sending email
from email.mime.text import MIMEText #for creating email messages
import logging #for logging errors and messages
import os #for file operations
import zipfile #for zipping files

#global variables

DB_NAME = "monitor-system.db"
CPU_THRESHOLD = 80.0  # Adjust as needed
CHECK_INTERVAL = 10    # How many seconds between checks
SENDER_EMAIL = "ofsnr31@gmail.com"
SENDER_PASSWORD = "5.5.5.1++a"
RECEIVER_EMAIL = "omerfaruksener045@gmail.com"

def create_db():
    """
    Creates the database and tables if they don't exist.
    """
    try:
        conn = sqlite3.connect(DB_NAME) #connect to database
        cur = conn.cursor() #create cursor object
        cur.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                ram_usage REAL
            )
        ''')
        conn.commit()
    except Exception as e:
        logging.error(f"Error creating database: {e}")
    finally:
        conn.close()

def collect_metrics():
    """
    Collects CPU and RAM usage using psutil.
    Returns:
        (float, float): A tuple containing (cpu_usage_percent, ram_usage_percent).
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        ram_usage = ram_info.percent
        return cpu_usage, ram_usage
    except Exception as e:
        logging.error(f"Error collecting metrics: {e}")
        return None, None

def insert_metrics(cpu_usage, ram_usage):
    """
    Inserts CPU and RAM usage into the database.
    """
    try:
        conn = sqlite3.connect(DB_NAME) #connect to database
        cur = conn.cursor() #create cursor object
        cur.execute('''
            INSERT INTO metrics (cpu_usage, ram_usage)
            VALUES (?, ?)
        ''', (cpu_usage, ram_usage))  #insert data into the database
        conn.commit() #commit the transaction
    except Exception as e:
        logging.error(f"Error inserting metrics: {e}")
    finally:
        conn.close() #close the connection


def send_email_alert(subject, body, sender_email, sender_password, receiver_email):
    """
    Sends an email alert.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Connect to Gmail's SSL SMTP server.
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Error sending email: {e}")

#spam-prevention-mechanism adding cooldown for email sending

def send_email_alert(subject, body, sender_email, sender_password, receiver_email):
    """
    Sends an email alert with a cooldown mechanism.
    """
    try:
        if time.time() - last_email_time < 60: #60 seconds cooldown
            return
        last_email_time = time.time()
        send_email_alert(subject, body, sender_email, sender_password, receiver_email)
    except Exception as e:
        logging.error(f"Error sending email: {e}")

#archive old db

def archive_old_db():
    """
    Archives the old database by renaming it with a timestamp. and deleting it if it's older than 30 days
    """
    try:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        os.rename(DB_NAME, f"{DB_NAME}.{timestamp}")
        #7z compression

        with zipfile.ZipFile(f"{DB_NAME}.{timestamp}.zip", "w") as zipf:
            zipf.write(f"{DB_NAME}.{timestamp}", arcname=f"{DB_NAME}.{timestamp}")
        logging.info(f"Old database archived: {DB_NAME}.{timestamp}")
        logging.info(f"Database archived: {DB_NAME}.{timestamp}.zip")
        #delete the old database if it's older than 30 days
        if os.path.exists(f"{DB_NAME}.{timestamp}"):
            os.remove(f"{DB_NAME}.{timestamp}")
            logging.info(f"Old database deleted: {DB_NAME}.{timestamp}")
    except Exception as e:
        logging.error(f"Error archiving database: {e}")

def main():
    """
    Main function to run the system monitor.
    """
    # 1) Create or verify the database
    create_db()

    # 2) Start an infinite loop to collect data periodically
    while True:
        # Collect CPU and RAM usage
        cpu_val, ram_val = collect_metrics()
        print(f"CPU: {cpu_val:.1f}% | RAM: {ram_val:.1f}%")

        # Store in the database
        insert_metrics(cpu_val, ram_val)

        # Check if CPU usage is beyond the threshold
        if cpu_val > CPU_THRESHOLD:
            subject = "CPU HIGH ALERT"
            body = f"CPU usage is {cpu_val:.1f}% which exceeds {CPU_THRESHOLD}%."
            send_email_alert(subject, body, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
            print("[ALERT] CPU usage is too high! Email sent.")

        # Sleep before the next check
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()