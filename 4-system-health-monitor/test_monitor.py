#!/usr/bin/env python3
"""
test_monitor.py

Run tests with:
  pytest test_monitor.py
"""

import os
import sqlite3
import pytest
import time
from unittest.mock import patch

# Monitor fonksiyonlarını import
from monitor import (
    DB_NAME,
    create_db,
    insert_metrics,
    collect_metrics,
    send_email_with_cooldown,
    LAST_EMAIL_TIME
)

@pytest.fixture
def setup_db():
    """
    Fixture: testten önce veritabanı (varsa) siler, create_db() çağırır.
    Test bitince de silebiliriz ama bazen arşivlemek isteyebilirsin.
    """
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    create_db()
    yield
    # Cleanup if desired:
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_collect_metrics():
    cpu_val, ram_val = collect_metrics()
    assert cpu_val is not None, "cpu_val should not be None"
    assert ram_val is not None, "ram_val should not be None"
    # Normalde CPU 0..100 arası, bazen 100'ü geçebiliyor (çok çekirdekli sistemlerde).
    # Yine de basit bir aralık testi:
    assert 0 <= cpu_val <= 150  
    assert 0 <= ram_val <= 100

def test_db_creation_and_insertion(setup_db):
    # DB oluşturulmuş olmalı
    assert os.path.exists(DB_NAME), "DB file should exist."

    insert_metrics(30.5, 45.2)
    insert_metrics(10.2, 99.9)

    # Kontrol
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT cpu_usage, ram_usage FROM metrics")
    rows = cur.fetchall()
    conn.close()

    assert len(rows) == 2
    assert rows[0] == (30.5, 45.2)
    assert rows[1] == (10.2, 99.9)

@patch("smtplib.SMTP_SSL") 
def test_send_email_with_cooldown(mock_smtp):
    """
    Test the cooldown logic by calling send_email_with_cooldown multiple times.
    """
    from monitor import LAST_EMAIL_TIME, send_email_with_cooldown
    # Sıfırlayalım
    # (Globali manipüle edeceğiz ama test izole ortamda olduğu için sorun olmaz.)
    import monitor
    monitor.LAST_EMAIL_TIME = 0.0

    # 1) First call => should send
    send_email_with_cooldown("Test Subject", "Test Body", cooldown=1)
    assert mock_smtp.called, "Should send on first call."
    mock_smtp.reset_mock()

    # 2) Immediate second call => should NOT send
    send_email_with_cooldown("Test Subject2", "Test Body2", cooldown=60)
    assert not mock_smtp.called, "Cooldown active, no second call."

    # 3) Wait > 1s => should send again
    time.sleep(1.1)
    send_email_with_cooldown("Test Subject3", "Test Body3", cooldown=1)
    assert mock_smtp.called, "Should send after cooldown."
