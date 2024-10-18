# Import library yang diperlukan
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timezone
import logging
import pytz

# Konfigurasi logger
timezone = pytz.timezone("Asia/Jakarta")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state, authorized_users  # Impor di dalam fungsi
    from config import connect_to_postgres
    from utils import get_site_name
    user = update.effective_user.id  # Mengambil user_id dengan efektif

    # Periksa user_state[user] user di dictionary
    if user not in user_state:
        user_state[user] = {
            "context": None,
            "menu": "start",
            "waiting_for_password": False,
            "site_name": "",
            "df": None
        }

    # Menghubungkan ke database
    conn = connect_to_postgres()

    if conn:
        df = get_site_name(conn)
        if df is not None:
            user_state[user]['df'] = df
            print(df)
        conn.close()
    else:
        await update.message.reply_text("Failed to connect to the database.")

    # Cek apakah user sudah authorized
    if user in authorized_users:
        await update.message.reply_text(
            "Please type directly the site name you want to know, or like this :\n@ioh_site_bot <site name>."
        )
    else:
        await update.message.reply_text("Please enter the password to proceed:")
        user_state[user]["waiting_for_password"] = True

# Fungsi untuk menangani perintah /end
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengakhiri sesi pengguna"""
    from main import user_state  # Impor di dalam fungsi
    user_id = update.effective_user.id
    if user_id in user_state:  # Menghapus user dari user_state jika ada
        del user_state[user_id]  # Hapus status user dari dictionary
    await update.message.reply_text("Your session has ended. Please use /start to begin again")
