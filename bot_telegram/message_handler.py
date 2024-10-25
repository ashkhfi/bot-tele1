# Import library yang diperlukan
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timezone
import logging
import pytz
from utils import check_password, log_to_csv, log_to_spreadsheet
from qa_system import answer_question
from config import connect_to_postgres
from data_handler import set_context

# Konfigurasi logger
timezone = pytz.timezone("Asia/Jakarta")
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context):
    from main import user_state, authorized_users  # Impor di dalam fungsi
    user = update.message.from_user.id
    user_id = update.message.from_user.id
    user_message = update.message.text.lower()  # Mengubah ke huruf kecil untuk mencocokkan
    # now = datetime.now(timezone.utc)
    now = datetime.now(timezone)
    message = update.message.text
    formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")

    if user_id not in authorized_users:
        await check_password(update, context)
        return

    # if user_state[user]['menu'] == 'profil':
    #     question = update.message.text
    #     answer = answer_question(question, user_state[user]['context'])
    #     keyboard = [
    #       [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
    #        InlineKeyboardButton("Show All Data", callback_data='data_profil')]
    #     ]
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     if answer == "":
    #         await update.message.reply_text("Sorry, I couldn't find an answer to your question.", reply_markup=reply_markup)
    #     else:
    #         await update.message.reply_text(answer, reply_markup=reply_markup)

    # if user_state[user]['menu'] == 'stat':
    #     question = update.message.text
    #     answer = answer_question(question, user_state[user]['context'])
    #     keyboard = [
    #       [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
    #        InlineKeyboardButton("Show All Data", callback_data='data_statistik')]
    #     ]
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     await update.message.reply_text(answer, reply_markup=reply_markup)

    if user_state[user]['menu'] == 'start':
        conn = connect_to_postgres()
        if conn:
            site_name = update.message.text
            user_state[user]['site_name'] = site_name
            user_state[user]['context'] = set_context(conn, site_name)

            if user_state[user]['context'] != "null":
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
            [InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
    if message and message != user_state[user]['site_name']:
        question = update.message.text
        answer = answer_question(message, user_state[user]['context'])
        print(answer)
        if answer:
            await update.message.reply_text(answer)
            
            first_name = update.message.from_user.first_name  # Nama depan
            last_name = update.message.from_user.last_name    # Nama belakang
            user_name = f"{first_name} {last_name}"   
            log_to_csv(user_name, question, answer)  
            log_to_spreadsheet(user_name, question, answer)  

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
