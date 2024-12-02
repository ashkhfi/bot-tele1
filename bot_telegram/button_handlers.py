from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode 
from telegram.ext import ContextTypes
from features.qa_system import answer_question
from utils import process_data
from config import connect_to_postgres
from features.chart_system import plot_data
from data_handler import get_data_chart
from features.sumarize_system import generate_summary_report
import os
import datetime

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state
    query = update.callback_query
    user = query.from_user.id
    await query.answer()

    if query.data == 'profile_site':
        user_state[user]['menu'] = 'profil'
        formatted_text = process_data(user_state[user]['context'])
        await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
        user_state[user]['menu'] = 'home'
        keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )


    elif query.data == 'maps':
        user_state[user]['menu'] = 'maps'
        coordinates = answer_question("coordinate?", user_state[user]['context'])
        if coordinates:
            await query.message.reply_text(f"{coordinates}")
            user_state[user]['menu'] = 'home'
        else:
            await query.message.reply_text(f"Coordinates not found.")
        
        keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )

    elif query.data == 'chart_site':
        user_state[user]['menu'] = 'chart'
        keyboard = [
                [InlineKeyboardButton("PRB", callback_data='prb_chart'),
                InlineKeyboardButton("EUT", callback_data='eut_chart')],
                [InlineKeyboardButton("Traffic", callback_data='traffic_chart'),
                InlineKeyboardButton("Availability", callback_data='availability_chart')],
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Please select the data", reply_markup=reply_markup)

    elif query.data == 'summarize':
        user_state[user]['menu'] = 'summary'
        conn = connect_to_postgres()
        if conn:
            df = get_data_chart(conn, user_state[user]['site_name'], 6)  
            if df.empty:
                await query.message.reply_text("No data found")
                user_state[user]['menu'] = 'home'
            else:
                a = generate_summary_report(df)
                await query.message.reply_text(a)
                user_state[user]['menu'] = 'home'
        else:
            await query.message.reply_text("Failed to connect database")
            user_state[user]['menu'] = 'home'
        keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )

    elif query.data == 'back_to_menu':
        user_state[user]['menu'] = 'home'
        user_state[user]["just_returned_home"] = True
        user_state[user]['chart'] = None
        user_state[user]['time_chart'] = None
        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile_site'),
            InlineKeyboardButton("Maps", callback_data='maps')],
            [InlineKeyboardButton("Chart", callback_data='chart_site'),
            InlineKeyboardButton("Summary", callback_data='summarize')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.reply_text(f"What do you want to know about {user_state[user]['site_name']}?", reply_markup=reply_markup)

    elif query.data == 'start':
        user_state[user]['menu'] = 'start'
        user_state[user]['context'] = "null"
        user_state[user]['site_name'] = None
        user_state[user]['chart'] = None
        user_state[user]['time_chart'] = None

        await query.message.reply_text("Please type directly the site name you want to know, or like this :\n@quicksite_bot <site name>.")
        
        
        # data chart
    elif query.data == 'prb_chart':
        # Plot data untuk 'prb_chart'
        print(user_state[user]['menu'])
        plot_data(
            user_state[user]['chart'], 
            'dl_prb', 
            f'PRB data of site {user_state[user]["site_name"]} Last 1 Month'
        )
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
                user_state[user]['menu'] = 'home'
                print(user_state[user]['menu'])
                keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )
            os.remove('chart.jpg')
            
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")
                

    elif query.data == 'availability_chart':
        plot_data(
        user_state[user]['chart'], 
        'availability', 
        f'Availability data of site {user_state[user]["site_name"]} Last 1 Month')
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
                user_state[user]['menu'] = 'home'
                keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )
            os.remove('chart.jpg')
            
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")

    elif query.data == 'eut_chart':
        plot_data(
        user_state[user]['chart'], 
        'eut', 
        f'EUT data of site {user_state[user]["site_name"]} Last 1 Month'
        )
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
                user_state[user]['menu'] = 'home'
                keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )
            os.remove('chart.jpg')
            
            
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")

    elif query.data == 'traffic_chart':
        plot_data(
        user_state[user]['chart'], 
        'traffic_gb', 
        f'Traffic data of site {user_state[user]["site_name"]} Last 1 Month'
        )
        if os.path.exists('chart.jpg'):
            with open('chart.jpg', 'rb') as chart_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=chart_file)
                user_state[user]['menu'] = 'home'
                keyboard = [
                                [InlineKeyboardButton("Profile", callback_data='profile_site'),
                                InlineKeyboardButton("Maps", callback_data='maps')],
                                [InlineKeyboardButton("Chart", callback_data='chart_site'),
                                InlineKeyboardButton("Summary", callback_data='summarize')],
                            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                                f"Please choose one of the menu below to get information about {user_state[user]['site_name']}:",
                                reply_markup=reply_markup
                            )
            os.remove('chart.jpg')
            
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate chart. Please try again.")
