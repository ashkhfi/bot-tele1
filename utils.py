import pandas as pd
import logging
from telegram import Update
from telegram.ext import ContextTypes
import re
from bot_telegram.commands import start

# Konfigurasi logger
logger = logging.getLogger(__name__)

# Fungsi untuk mengimpor variabel yang diperlukan dari main
def get_main_variables():
    from main import user_state, authorized_users, PASSWORD_1, PASSWORD_2
    return user_state, authorized_users, PASSWORD_1, PASSWORD_2

async def check_password(update: Update, context):
    user_state, authorized_users, PASSWORD_1, PASSWORD_2 = get_main_variables()
    
    # Ambil user_id dari pesan
    user_id = update.message.from_user.id
    user_password = update.message.text

    # Periksa apakah user sedang menunggu password
    if user_state[user_id]["waiting_for_password"]:
        if user_password == PASSWORD_1 or user_password == PASSWORD_2:
            # Tambahkan user ke daftar authorized_users
            authorized_users.add(user_id)
            user_state[user_id]["waiting_for_password"] = False
            await update.message.reply_text("Password accepted! You now have access.")
            await start(update, context)  # Panggil start atau proses lainnya
        else:
            await update.message.reply_text("Incorrect password. Please try again:")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def get_site_name(conn):
    query = "SELECT DISTINCT site_name, site_id FROM magang_dataset;"
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error saat mengambil data: {e}")
        return None

def process_data(data_string, return_type='profile'):
    # Mengonversi string menjadi dictionary
    data_dict = {}
    for item in data_string.split(';'):
        if item.strip():  # Mengabaikan string kosong
            key, value = item.split(':', 1)
            data_dict[key.strip()] = value.strip()

    # Menyusun data profil dan statistik ke dalam dua variabel terpisah dengan nilai diapit <b>
    profile_data = (
        f"site name: <b>{data_dict['site_name']}</b>\n"
        f"enodeb id: <b>{data_dict['enodeb_id']}</b>\n"
        f"site id: <b>{data_dict['site_id']}</b>\n"
        f"mc: <b>{data_dict['mc']}</b>\n"
        f"region: <b>{data_dict['region']}</b>\n"
        f"regency: <b>{data_dict['kabupaten']}</b>\n"
        f"tac: <b>{data_dict['tac']}</b>\n"
        f"transport: <b>{data_dict['transport']}</b>\n"
        f"azimuth: <b>{data_dict['azimuth']}</b>\n"
        f"hub type: <b>{data_dict['hub_type']}</b>\n"
        f"field type: <b>{data_dict['field_type']}</b>\n"
        f"site class: <b>{data_dict['site_class']}</b>\n"
        f"hostname: <b>{data_dict['hostname']}</b>\n"
        f"antenna height: <b>{data_dict['antenna_height']}</b>\n"
        f"number cell congested: <b>{data_dict['number_cell_congested']}</b>\n"
        f"category: <b>{data_dict['category']}</b>\n"
    )

    statistical_data = (
        f"traffic 3id: <b>{data_dict['traffic_3id']}</b>\n"
        f"traffic  im3: <b>{data_dict['traffic_im3']}</b>\n"
        f"total traffic(GB): <b>{data_dict['total_traffic_gb']}</b>\n"
        f"prb: <b>{data_dict['prb']}</b>\n"
        f"eut: <b>{data_dict['eut']}</b>\n"
        f"ran config: <b>{data_dict['ran_config']}</b>"
    )

    # Menggabungkan keduanya dalam satu variabel sesuai return_type
    if return_type == 'profile':
        return profile_data
    elif return_type == 'statistical':
        return statistical_data
    else:
        return "Invalid return type specified. Use 'profile' or 'statistical'."

def answer_question_profil(question, context_profil):
    # Logika untuk menjawab pertanyaan tentang profil
    if "profile" in question.lower():
        return f"Profile info: {context_profil}"
    return "No relevant profile information found."

def answer_question_statistik(question, context_statistik):
    # Logika untuk menjawab pertanyaan tentang statistik
    if "traffic" in question.lower():
        return f"Statistic info: {context_statistik}"
    return "No relevant statistic information found."

def is_coordinate(coord_str):
    pattern = r'^-?\s*[1-8]?\s*[0-9]\s*(?:\.\s*\d+)?\s*,\s*-?\s*(?:[1-9]?[0-9]|1[0-7][0-9]|180)\s*(?:\.\s*\d+)?$'
    match = re.match(pattern, coord_str)
    return bool(match)