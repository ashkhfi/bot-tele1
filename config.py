import logging
import pytz
import psycopg2
from logging.handlers import RotatingFileHandler
from datetime import datetime


def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            user="postgres",  # Ganti dengan username PostgreSQL
            password="Solo987@!",  # Ganti dengan password PostgreSQL
            host="1.tcp.ap.ngrok.io",  # Ganti dengan host yang benar
            port="21674",  # Ganti dengan port yang benar
            database="npmcj"  # Ganti dengan nama database
        )
        return conn
    except Exception as e:
        print(f"Gagal terhubung ke database: {e}")
        return None
