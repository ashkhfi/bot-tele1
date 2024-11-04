# Import library yang diperlukan
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timezone
import logging
import pytz
import re
from utils import check_password, log_to_csv, log_to_spreadsheet
from features.qa_system import answer_question
from config import connect_to_postgres
from data_handler import set_context

# Konfigurasi logger
timezone = pytz.timezone("Asia/Jakarta")
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context):
    from main import user_state, authorized_users  # Impor di dalam fungsi
    user = update.message.from_user.id
    user_id = update.message.from_user.id
    message = update.message.text

    
    if user_id not in authorized_users:
        await check_password(update, context)
        return

    if user_state[user]['menu'] == 'start':
        conn = connect_to_postgres()
        if conn:
            input_value = update.message.text.upper()  # Mengubah nilai input menjadi uppercase
            print(f"Input diterima: {input_value}")
            site_id_pattern = r'^\d{2}[A-Z]{3}\d{4}$'
            if re.match(site_id_pattern, input_value):  
                site_id = input_value.upper() 
                print(f"Mendeteksi site_id: {site_id}")
                df = user_state[user]['df']
                user_state[user]['site_id'] = site_id
                print(user_state[user]['site_id'])
                site_row = df[df['site_id'] == site_id]
                if not site_row.empty:
                    site_name = site_row.iloc[0]['site_name'].upper() 
                    user_state[user]['site_name'] = site_name
                    user_state[user]['context'] = set_context(conn, site_name)
                    print(f"Site ID: {site_id} ditemukan. Nama situs: {site_name}")
                else:
                    await update.message.reply_text("Site not found")
                    print('site name tidak ditemukan')
                    print(f"Site ID: {site_id} tidak ditemukan dalam DataFrame.") 
            else:
                #menggunakan site name
                site_name = input_value.upper() 
                user_state[user]['site_name'] = site_name

                df = user_state[user]['df']
                if df is not None and not df.empty:
                    # Cari baris yang memiliki `site_name` yang sesuai
                    matching_site = df[df['site_name'].str.lower() == site_name.lower()]

                    if not matching_site.empty:
                        site_id = matching_site.iloc[0]['site_id'].upper() 
                        user_state[user]['site_id'] = site_id
                        print(f"Site ID {site_id} ditemukan untuk site_name '{site_name}'.")
                    else:
                        print(f"Tidak ada data yang cocok untuk site_name '{site_name}'.")
                else:
                    print("DataFrame pengguna tidak tersedia atau kosong.")

                # Set context berdasarkan `site_name`
                user_state[user]['context'] = set_context(conn, site_name)
                print(f"Nama situs: {site_name} diterima dan konteks telah disetel.")


            if user_state[user]['context'] != None:
                user_state[user]['menu'] = 'home'
                user_state[user]["just_returned_home"] = True
            else:       
                await update.message.reply_text("site not found")
            conn.close()
        else:
            await update.message.reply_text("Connection to database failed.")

    if user_state[user]["menu"] == "home":
        message = update.message.text
        # Membuat keyboard menu
        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile_site'),
            InlineKeyboardButton("Stats", callback_data='statistics'),
            InlineKeyboardButton("Maps", callback_data='maps')],
            [InlineKeyboardButton("Chart", callback_data='chart_site'),
            InlineKeyboardButton("Summary", callback_data='summarize')],
            # [InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
    if message and message != user_state[user]['site_name'] and message != user_state[user]['site_id']:
        print(f'pesan : {message}')
        if user in user_state:
            if 'site_name' in user_state[user]:
                print(f'site name : {user_state[user]["site_name"]}')
            else:
                print("site_name belum diinisialisasi.")

            if 'site_id' in user_state[user]:
                print(f'site id : {user_state[user]["site_id"]}')
            else:
                print("site_id belum diinisialisasi.")
        else:
            print("User belum terdaftar di user_state.")

        question = update.message.text.upper()
        if question and question != user_state[user]['site_name'] and question != user_state[user]['site_id'] : 
            answer = answer_question(message, user_state[user]['context'])
            print(answer)
            if answer:
                await update.message.reply_text(answer)
                
                first_name = update.message.from_user.first_name  # Nama depan
                last_name = update.message.from_user.last_name    # Nama belakang
                user_name = f"{first_name} {last_name}"   
                log_to_csv(user_name, question, answer)  
                log_to_spreadsheet(user_name, question, answer, user_state[user]['password_access'])  

            else:
                await update.message.reply_text(
                    f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                    reply_markup=reply_markup
                )

        
    if user_state[user].get("just_returned_home", False):
        await update.message.reply_text(
            f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:", 
            reply_markup=reply_markup
        )
        user_state[user]["just_returned_home"] = False
