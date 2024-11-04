from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode 
from telegram.ext import ContextTypes
from features.qa_system import answer_question
from utils import process_data
from config import connect_to_postgres
from features.chart_system import plot_data
from data_handler import get_data_chart, get_data_sumarize
from features.sumarize_system import summarize_issues
import os
import datetime

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state
    query = update.callback_query
    user = query.from_user.id
    await query.answer()

    if query.data == 'profile_site':
        user_state[user]['menu'] = 'profil'
        formatted_text = process_data(user_state[user]['context'], return_type='profile')
        await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'statistics':
        user_state[user]['menu'] = 'stat'
        formatted_text = process_data(user_state[user]['context'], return_type='statistical')
        await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'maps':
        user_state[user]['menu'] = 'maps'
        coordinates = answer_question("coordinate?", user_state[user]['context'])
        if coordinates:
            await query.message.reply_text(f"{coordinates}")
            # Inline keyboard for maps
            keyboard = [
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]  
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await query.message.reply_text(f"Coordinates not found.")

    elif query.data == 'chart_site':
        user_state[user]['menu'] = 'chart'
        user_message = update.message.text.lower()
    
        # Cek apakah `update` memiliki callback query atau tidak
        query = update.callback_query
    
        # Jika `query` ada (dari tombol), lanjutkan ke proses callback
        if query:
            await query.answer()  # Mengkonfirmasi bahwa query diterima
            query.data = 'chart'  # Atur data callback ke 'chart_site'
        # await query.message.reply_text("This feature is still maintenance")
        # keyboard = [
        #   [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
        #    InlineKeyboardButton("Back to Start", callback_data='start')]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        keyboard = [
          [InlineKeyboardButton("7 Days", callback_data='7_days'),
           InlineKeyboardButton("14 Days", callback_data='14_days'),
           InlineKeyboardButton("1 Month", callback_data='1_month')],
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Please select a time range", reply_markup=reply_markup)
    elif query.data == 'summarize':
        user_state[user]['menu'] = 'summary'
        conn = connect_to_postgres()
        if conn:
            df = get_data_sumarize(conn, user_state[user]['site_name'])  # Mendapatkan data 7 hari terakhir
            if df.empty:
                await query.message.reply_text("No data found")
            else:
                a = summarize_issues(df)
                await query.message.reply_text(a['message'])
        else:
            await query.message.reply_text("Failed to connect database")

        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'back_to_menu':
        user_state[user]['menu'] = 'home'
        user_state[user]["just_returned_home"] = True
        user_state[user]['chart'] = None
        user_state[user]['time_chart'] = None
        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile_site'),
            InlineKeyboardButton("Stats", callback_data='statistics'),
            InlineKeyboardButton("Maps", callback_data='maps')],
            [InlineKeyboardButton("Chart", callback_data='chart_site'),
            InlineKeyboardButton("Summary", callback_data='summarize')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"What do you want to know about {user_state[user]['site_name']}?", reply_markup=reply_markup)


    elif query.data == 'start':
        user_state[user]['menu'] = 'start'
        user_state[user]['context'] = "null"
        user_state[user]['site_name'] = None
        user_state[user]['chart'] = None
        user_state[user]['time_chart'] = None

        await query.message.reply_text("Please type directly the site name you want to know, or like this :\n@ioh_site_bot <site name>.")

    # elif query.data == 'data_profil':
    #     formatted_text = process_data(user_state[user]['context'], return_type='profile')
    #     await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
    #     keyboard = [
    #       [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
    #        InlineKeyboardButton("Back to Start", callback_data='start')]
    #     ]
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    # elif query.data == 'data_statistik':
    #     formatted_text = process_data(user_state[user]['context'], return_type='statistical')
    #     await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
    #     keyboard = [
    #       [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
    #        InlineKeyboardButton("Back to Start", callback_data='start')]
    #     ]
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    ##chart
    elif query.data == '7_days':
        user_state[user]['time_chart'] = 7
        conn = connect_to_postgres()
        if conn:
            user_state[user]['chart'] = get_data_chart(conn, user_state[user]['site_name'], 7)  # Mendapatkan data 7 hari terakhir
            if user_state[user]['chart'].empty:
                keyboard = [
                [InlineKeyboardButton("7 Days", callback_data='7_days'),
                InlineKeyboardButton("14 Days", callback_data='14_days'),
                InlineKeyboardButton("1 Month", callback_data='1_month')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.reply_text("data not found", reply_markup=reply_markup)
            else:
                
                keyboard = [
                [InlineKeyboardButton("PRB", callback_data='prb_chart'),
                InlineKeyboardButton("EUT", callback_data='eut_chart')],
                [InlineKeyboardButton("Traffic", callback_data='traffic_chart'),
                InlineKeyboardButton("Availability", callback_data='availability_chart')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text("Please select the data", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Connection to database failed.")
  

    elif query.data == '14_days':
        user_state[user]['time_chart'] = 14
        conn = connect_to_postgres()
        if conn:
            user_state[user]['chart'] = get_data_chart(conn, user_state[user]['site_name'], 14)  # Mendapatkan data 7 hari terakhir
            if user_state[user]['chart'].empty:
                keyboard = [
                [InlineKeyboardButton("7 Days", callback_data='7_days'),
                InlineKeyboardButton("14 Days", callback_data='14_days'),
                InlineKeyboardButton("1 Month", callback_data='1_month')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.reply_text("data not found", reply_markup=reply_markup)
            else:
                
                keyboard = [
                [InlineKeyboardButton("PRB", callback_data='prb_chart'),
                InlineKeyboardButton("EUT", callback_data='eut_chart')],
                [InlineKeyboardButton("Traffic", callback_data='traffic_chart'),
                InlineKeyboardButton("Availability", callback_data='availability_chart')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text("Please select the data", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Connection to database failed.")
  

    elif query.data == '1_month':
        user_state[user]['time_chart'] = 30
        conn = connect_to_postgres()
        if conn:
            user_state[user]['chart'] = get_data_chart(conn, user_state[user]['site_name'], 30)  # Mendapatkan data 7 hari terakhir
            if user_state[user]['chart'].empty:
                keyboard = [
                [InlineKeyboardButton("7 Days", callback_data='7_days'),
                InlineKeyboardButton("14 Days", callback_data='14_days'),
                InlineKeyboardButton("1 Month", callback_data='1_month')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.reply_text("data not found", reply_markup=reply_markup)
            else:
                
                keyboard = [
                [InlineKeyboardButton("PRB", callback_data='prb_chart'),
                InlineKeyboardButton("EUT", callback_data='eut_chart')],
                [InlineKeyboardButton("Traffic", callback_data='traffic_chart'),
                InlineKeyboardButton("Availability", callback_data='availability_chart')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text("Please select the data", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Connection to database failed.")
  


        # data chart
    elif query.data == 'prb_chart':
        # Plot data untuk 'prb_chart'
        plot_data(
            user_state[user]['chart'], 
            'dl_prb', 
            f'PRB data of site {user_state[user]["site_name"]} Last {user_state[user]["time_chart"]} Days'
        )

        # Cek apakah file 'chart.jpg' berhasil dibuat
        if os.path.exists('chart.jpg'):
            try:
                with open('chart.jpg', 'rb') as chart_file:
                    # Kirim file chart ke pengguna
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
            except Exception as e:
                await context.bot.send_message(chat_id=query.message.chat_id, text=f"Error while sending chart: {e}")
            finally:
                # Hapus file setelah dikirim
                if os.path.exists('chart.jpg'):
                    try:
                        os.remove('chart.jpg')
                    except Exception as e:
                        await context.bot.send_message(chat_id=query.message.chat_id, text=f"Error while deleting chart: {e}")
            
            # Tampilkan keyboard setelah mengirim chart
            keyboard = [
                [InlineKeyboardButton("Back to Time Range", callback_data='chart_site')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")


    elif query.data == 'availability_chart':
        plot_data(
        user_state[user]['chart'], 
        'availability', 
        f'Availability data of site {user_state[user]["site_name"]} Last {user_state[user]["time_chart"]} Days'
        )

        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
            os.remove('chart.jpg')
             # Tambahkan keyboard setelah mengirim chart
            keyboard = [
                [InlineKeyboardButton("Back to Time Range", callback_data='chart_site')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")

    elif query.data == 'eut_chart':
        plot_data(
        user_state[user]['chart'], 
        'eut', 
        f'EUT data of site {user_state[user]["site_name"]} Last {user_state[user]["time_chart"]} Days'
        )
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
            os.remove('chart.jpg')
             # Tambahkan keyboard setelah mengirim chart
            keyboard = [
                [InlineKeyboardButton("Back to Time Range", callback_data='chart_site')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")

    elif query.data == 'traffic_chart':
        plot_data(
        user_state[user]['chart'], 
        'traffic_gb', 
        f'Traffic data of site {user_state[user]["site_name"]} Last {user_state[user]["time_chart"]} Days'
        )
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
            os.remove('chart.jpg')
             # Tambahkan keyboard setelah mengirim chart
            keyboard = [
                [InlineKeyboardButton("Back to Time Range", callback_data='chart_site')],
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")
