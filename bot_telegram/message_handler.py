# Import library yang diperlukan
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timezone
import logging
import pytz
import re
from utils import check_password, log_to_spreadsheet, contains_any_emoji
from features.qa_system import answer_question

from config import connect_to_postgres
from data_handler import set_context, get_data_chart
from .button_handlers import button
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import emoji
# Konfigurasi logger
timezone = pytz.timezone("Asia/Jakarta")
logger = logging.getLogger(__name__)

def get_closest_matches(user_input, choices, limit=1):
    matches = process.extract(user_input, choices, scorer=fuzz.ratio, limit=limit)
    filtered_matches = [match for match, score in matches if score > 70]
    return filtered_matches

async def handle_message(update: Update, context):
    from main import user_state, authorized_users  # Impor di dalam fungsi
    user = update.message.from_user.id
    user_id = update.message.from_user.id
    message = update.message.text

    
    if user_id not in authorized_users:
        await check_password(update, context)
        return


    #set context
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
                    user_state[user]['chart'] = get_data_chart(conn, site_name, 31) 
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
                        user_state[user]['context'] = set_context(conn, site_name)
                        user_state[user]['chart'] = get_data_chart(conn, site_name, 31) 
                        print(f"Site ID {site_id} ditemukan untuk site_name '{site_name}'.")
                    else:
                        print(f"Tidak ada data yang cocok untuk site_name '{site_name}'.")
                else:
                    print("DataFrame pengguna tidak tersedia atau kosong.")

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
        sitename_closest_matches = None
        siteid_closest_matches = None
        
        if message.upper() in user_state[user]['site_name_list'] and message.upper() != user_state[user]['site_name'] and message.upper() != user_state[user]['site_id']:
            await update.message.reply_text("You can move sites with the /site command!")
        elif message.upper() in user_state[user]['site_id_list'] and message.upper() != user_state[user]['site_name'] and message.upper() != user_state[user]['site_id']:
            await update.message.reply_text("You can move sites with the /site command!")
        else:
            if message.upper() not in user_state[user]['site_name_list'] and message.upper() not in user_state[user]['site_id_list']:
                sitename_closest_matches = get_closest_matches(message.upper(), user_state[user]['site_name_list'])
                siteid_closest_matches = get_closest_matches(message.upper(), user_state[user]['site_id_list'])
                
                if sitename_closest_matches:
                    suggestions = ", ".join(sitename_closest_matches)
                    await update.message.reply_text(
                        f"Did you mean: `{suggestions}`?\n\n *Note: You can copy the suggestion above to the clipboard*",
                        parse_mode='MarkdownV2'
                    )

                elif siteid_closest_matches:
                    suggestions = ", ".join(siteid_closest_matches)
                    await update.message.reply_text(
                        f"Did you mean: `{suggestions}`?\n\n *Note: You can copy the suggestion above to the clipboard*",
                        parse_mode='MarkdownV2'
                    )

                else:

                    keywords_chart = ["chart", "graph", "trend", "tren"]
                    keywords_nearest = ["surrounding", "near", "nearest"]
                    keywords_home = ["home", "menu"]
                    keywords_help = ["help", "help?"]

                    #menangani inputan yang berhubungan dengan chart
                    if any(keyword in message.lower() for keyword in keywords_chart):
                        await handle_chart(update, context)
                        return  
                    
                    #menangani inputan yang berhubungan nearest site
                    elif any(keyword in message.lower() for keyword in keywords_nearest):
                        await update.message.reply_text("to use the feature to find the nearest site you can use the /site command")
                    
                    #menangani inputan yang berhubungan help
                    elif any(keyword in message.lower() for keyword in keywords_help):
                        await update.message.reply_text("Use the /help command to view the bot guide")
                    
                    #menangani inputan yang berhubungan dengan home atau menu untuk memunculkan menu
                    elif any(keyword in message.lower() for keyword in keywords_home):
                        keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Stats", callback_data='statistics'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await update.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )

                    #menangani inputan emoji
                    elif contains_any_emoji(message): 
                        await update.message.reply_text("not allowed to input emoticons!!!")
                        return  
                    
                    else:
                        #model menjawab pertanyaan dari user
                        question = update.message.text.upper()
                        answer = answer_question(message, user_state[user]['context'])
                        print(answer)
                        
                        if answer:
                            await update.message.reply_text(answer)
                            first_name = update.message.from_user.first_name  # Nama depan
                            last_name = update.message.from_user.last_name    # Nama belakang
                            user_name = f"{first_name} {last_name}"   
                            log_to_spreadsheet(user_name, question, answer, user_state[user]['password_access'], user_state[user]['site_name'])
                        else:
                            keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Stats", callback_data='statistics'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            await update.message.reply_text("Answer not found")
                            await update.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )

                    
    if user_state[user].get("just_returned_home", False):
        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile_site'),
            InlineKeyboardButton("Stats", callback_data='statistics'),
            InlineKeyboardButton("Maps", callback_data='maps')],
            [InlineKeyboardButton("Chart", callback_data='chart_site'),
            InlineKeyboardButton("Summary", callback_data='summarize')],
            # [InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:", 
            reply_markup=reply_markup
        )
        user_state[user]["just_returned_home"] = False

async def handle_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_message = update.message.text.lower()
    
    # Cek apakah `update` memiliki callback query atau tidak
    query = update.callback_query
    
    # Jika `query` ada (dari tombol), lanjutkan ke proses callback
    if query:
        await query.answer()  # Mengkonfirmasi bahwa query diterima
        query.data = 'chart'  # Atur data callback ke 'chart_site'
    
    # Tampilan menu chart untuk pengguna
    keyboard = [
                [InlineKeyboardButton("PRB", callback_data='prb_chart'),
                InlineKeyboardButton("EUT", callback_data='eut_chart')],
                [InlineKeyboardButton("Traffic", callback_data='traffic_chart'),
                InlineKeyboardButton("Availability", callback_data='availability_chart')],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Please select the data", reply_markup=reply_markup)

