import logging
import pytz
import psycopg2
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Fungsi untuk custom log formatting ke CSV

timezone = pytz.timezone("Asia/Jakarta")  # Ganti dengan zona waktu Anda
class CsvFormatter(logging.Formatter):
    def format(self, record):
        now = datetime.now(timezone)
        record.asctime = now.strftime('%Y-%m-%d %H:%M:%S %Z')  # Menambahkan timezone ke asctime
        return f'{record.asctime},{record.levelname},{record.message}'

# Fungsi konfigurasi logging untuk console dan file CSV
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Formatter untuk logging di console
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S %Z')
    
    # Tambahkan console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Formatter untuk logging ke file CSV
    csv_formatter = CsvFormatter()

    # Buat file handler untuk CSV (rotasi jika file besar)
    file_handler = RotatingFileHandler('log_output.csv', mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
    file_handler.setFormatter(csv_formatter)
    logger.addHandler(file_handler)

# Panggil fungsi setup_logging() di awal program
setup_logging()

def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            user="xxx",  # Ganti dengan username PostgreSQL
            password="xxx",  # Ganti dengan password PostgreSQL
            host="xxxx",  # Ganti dengan host yang benar
            port="xxx",  # Ganti dengan port yang benar
            database="xxx"  # Ganti dengan nama database
        )
        return conn
    except Exception as e:
        logger.error(f"Gagal terhubung ke database: {e}")
        return None
