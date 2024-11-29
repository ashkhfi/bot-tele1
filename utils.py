import pandas as pd
import logging
from telegram import Update
from telegram.ext import ContextTypes
import re
import datetime
import gspread
from google.oauth2.service_account import Credentials
import os
import csv
from bot_telegram.commands import start
import emoji

logger = logging.getLogger(__name__)

# Fungsi untuk mengimpor variabel yang diperlukan dari main
def get_main_variables():
    from main import user_state, authorized_users, PASSWORD_1, PASSWORD_2, PASSWORD_3
    return user_state, authorized_users, PASSWORD_1, PASSWORD_2, PASSWORD_3

async def check_password(update: Update, context):
    user_state, authorized_users, PASSWORD_1, PASSWORD_2, PASSWORD_3 = get_main_variables()
    
    # Ambil user_id dari pesan
    user_id = update.message.from_user.id
    user_password = update.message.text

    # Periksa apakah user sedang menunggu password
    if user_state[user_id]["waiting_for_password"]:
        if user_password == PASSWORD_1 or user_password == PASSWORD_2 or user_password == PASSWORD_3:
            authorized_users.add(user_id)
            user_state[user_id]["password_access"] = user_password
            user_state[user_id]["waiting_for_password"] = False
            await update.message.reply_text("Password accepted! You now have access.")
            await start(update, context)
        else:
            await update.message.reply_text("Incorrect password. Please try again:")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def get_site_name(conn):
    query = "SELECT DISTINCT site_name, site_id, coordinate, enodeb_id FROM magang_dataset;"
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error saat mengambil data: {e}")
        return None

def process_data(data_string):
    # Mengonversi string menjadi dictionary
    data_dict = {}
    for item in data_string.split(';'):
        if ':' in item:  # Memastikan item memiliki karakter ':'
            key, value = item.split(':', 1)
            data_dict[key.strip()] = value.strip()
        elif item.strip():  # Menangani item yang tidak sesuai format tetapi tidak kosong
            print(f"Warning: Item '{item}' tidak sesuai format 'key:value' dan akan diabaikan.")

    try:
        all_data = (
            f"site name: <b>{data_dict.get('site_name', 'N/A')}</b>\n"
            f"enodeb id: <b>{data_dict.get('enodeb_id', 'N/A')}</b>\n"
            f"site id: <b>{data_dict.get('site_id', 'N/A')}</b>\n"
            f"mc: <b>{data_dict.get('mc', 'N/A')}</b>\n"
            f"region: <b>{data_dict.get('region', 'N/A')}</b>\n"
            f"regency: <b>{data_dict.get('regency', 'N/A')}</b>\n"
            f"coordinate: <b>{data_dict.get('coordinate', 'N/A')}</b>\n"
            f"tac: <b>{data_dict.get('tac', 'N/A')}</b>\n"
            f"antenna height: <b>{data_dict.get('antenna_height', 'N/A')}</b>\n"
            f"hostname: <b>{data_dict.get('hostname', 'N/A')}</b>\n"
            f"site class: <b>{data_dict.get('site_class', 'N/A')}</b>\n"
            f"transport: <b>{data_dict.get('transport', 'N/A')}</b>\n"
            f"azimuth: <b>{data_dict.get('azimuth', 'N/A')}</b>\n"
            f"hub type: <b>{data_dict.get('hub_type', 'N/A')}</b>\n"
            f"field type: <b>{data_dict.get('field_type', 'N/A')}</b>\n"
            f"category: <b>{data_dict.get('category', 'N/A')}</b>\n"
            f"number cell congested: <b>{data_dict.get('number_cell_congested', 'N/A')}</b>\n"
            f"traffic 3id: <b>{data_dict.get('traffic_3id', 'N/A')}</b>\n"
            f"traffic im3: <b>{data_dict.get('traffic_im3', 'N/A')}</b>\n"
            f"total traffic(GB): <b>{data_dict.get('total_traffic_gb', 'N/A')}</b>\n"
            f"prb: <b>{data_dict.get('prb', 'N/A')}</b>\n"
            f"eut: <b>{data_dict.get('eut', 'N/A')}</b>\n"
            f"ran config: <b>{data_dict.get('ran_config', 'N/A')}</b>\n"
            f"recti qty: <b>{data_dict.get('recti_qty', 'N/A')}</b>\n"
            f"battery bank: <b>{data_dict.get('battery_bank', 'N/A')}</b>\n"
            f"backup category: <b>{data_dict.get('backup_category', 'N/A')}</b>\n"
            f"pln cap: <b>{data_dict.get('pln_cap', 'N/A')}</b>\n"
            f"billing pln: <b>{data_dict.get('billing_pln', 'N/A')}</b>\n"
            f"vlr subs 3id: <b>{data_dict.get('vlr_subs_3id', 'N/A')}</b>\n"
            f"vlr subs im3: <b>{data_dict.get('vlr_subs_im3', 'N/A')}</b>\n"
            f"vlr subs ioh: <b>{data_dict.get('vlr_subs_ioh', 'N/A')}</b>\n"
            f"rev ioh: <b>{data_dict.get('rev_ioh', 'N/A')}</b>\n"
            f"rev im3: <b>{data_dict.get('rev_im3', 'N/A')}</b>\n"
            f"rev 3id: <b>{data_dict.get('rev_3id', 'N/A')}</b>\n"
        )
        return all_data
    except KeyError as e:
        # Menangani jika ada key yang hilang di data_dict
        return f"Error: Key {str(e)} tidak ditemukan di data. Pastikan format data sudah benar."


def is_coordinate(coord_str):
    pattern = r'^-?\s*[1-8]?\s*[0-9]\s*(?:\.\s*\d+)?\s*,\s*-?\s*(?:[1-9]?[0-9]|1[0-7][0-9]|180)\s*(?:\.\s*\d+)?$'
    match = re.match(pattern, coord_str)
    return bool(match)


def log_to_spreadsheet(user, question, answer, password, site):
    try:
        # Definisikan scope dan autentikasi
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('chatbot-ai-9b525-d61b3ea81a47.json', scopes=scope)
        client = gspread.authorize(creds)

        try:
            # Buka atau buat spreadsheet
            spreadsheet = client.open('log user')
            print(f"Spreadsheet 'log user' ditemukan.")
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create('log user')
            print(f"Spreadsheet baru 'log user' berhasil dibuat.")

        # Bagikan spreadsheet dengan email "ioh.chatbot@gmail.com"
        # spreadsheet.share("ioh.chatbot@gmail.com", perm_type='user', role='writer')
        # print("Spreadsheet telah dibagikan dengan akses editor ke 'ioh.chatbot@gmail.com'.")

        # # Ambil link untuk akses
        # spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        # print(f"Spreadsheet URL: {spreadsheet_url}")

        # Pilih worksheet dan tambahkan data
        worksheet = spreadsheet.sheet1
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_data = [user, password, current_date,site, question, answer]
        worksheet.append_row(log_data)
        print("Data berhasil disimpan ke Google Sheets!")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def contains_any_emoji(text):
    """
    Memeriksa apakah string mengandung setidaknya satu emoji.
    """
    return any(emoji.is_emoji(char) for char in text)
