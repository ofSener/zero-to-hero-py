# Python Monitoring with Encrypted Credentials

This project periodically collects CPU and RAM usage, stores the data in SQLite, and sends alert emails via Gmail when usage exceeds a threshold. It uses **Fernet encryption** to store sensitive credentials in a `.env` file, protecting them from accidental exposure.

## How It Works

1. **.env File**  
   
     APP_KEY=
     ENC_SENDER_EMAIL=...
     ENC_SENDER_PASSWORD=...
     ENC_RECEIVER_EMAIL=...
     ```

3. **Monitoring Script (`monitor.py`)**  
   - Loads `.env` via `python-dotenv`.  
   - Decrypts credentials using your Fernet key.  
   - Collects CPU/RAM usage with `psutil`.  
   - Inserts data into `monitor_system.db`.  
   - On high CPU usage, triggers `send_email_with_cooldown`, preventing spam.

4. **Logging**  
   - Logs go to `monitor.log` and console with timestamps and levels.

5. **Archiving**  
   - `archive_old_db()` function can rename and zip your DB, removing older archives beyond 30 days.


