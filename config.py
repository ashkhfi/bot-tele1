import logging
import pytz
import psycopg2

# Konfigurasi logging
timezone = pytz.timezone("Asia/Jakarta")  # Ganti dengan zona waktu Anda
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
#hfjfjfkkl
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
        logger.error(f"Gagal terhubung ke database: {e}")
        return None
