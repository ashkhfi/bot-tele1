from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode 
from telegram.ext import ContextTypes
from qa_system import answer_question
from utils import process_data

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state
    query = update.callback_query
    user = query.from_user.id
    await query.answer()

    if query.data == 'profile_site':
        user_state[user]['menu'] = 'profil'
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Show All Data", callback_data='data_profil')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("You can ask about profile data site  here by typing what data you want to know or click the *Show All Data* button to display all the data", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    elif query.data == 'statistics':
        user_state[user]['menu'] = 'stat'
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Show All Data", callback_data='data_statistik')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("You can ask about statistic data site here by typing what data you want to know or click the *Show All Data* button to display all the data", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    elif query.data == 'maps':
        user_state[user]['menu'] = 'maps'
        coordinates = answer_question("coordinate?", user_state[user]['context'])
        if coordinates:
            await query.message.reply_text(f"{coordinates}")
            # Inline keyboard for maps
            keyboard = [
                [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
                 InlineKeyboardButton("Back to Start", callback_data='start')]  
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        else:
            await query.message.reply_text(f"Coordinates not found.")

    elif query.data == 'chart_site':
        user_state[user]['menu'] = 'chart'
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
        # keyboard = [
        #      [
        #         InlineKeyboardButton("Availability", callback_data='availability'),
        #         InlineKeyboardButton("EUT", callback_data='eut')
        #      ],
        #      [
        #         InlineKeyboardButton("Traffic GB", callback_data='traffic_gb'),
        #         InlineKeyboardButton("DL PRB", callback_data='dl_prb')
        #     ],
        #     [
        #         InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')
        #     ]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # await query.edit_message_text(f"Please select a category Chart data of site '{user_state[user]['site_name']}':", reply_markup=reply_markup)
#a

    elif query.data == 'summarize':
        user_state[user]['menu'] = 'summary'
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)


    elif query.data == 'back_to_menu':
        user_state[user]['menu'] = 'home'
        user_state[user]["just_returned_home"] = True
        keyboard = [
            [InlineKeyboardButton("Profile", callback_data='profile_site'),
            InlineKeyboardButton("Stats", callback_data='statistics'),
            InlineKeyboardButton("Maps", callback_data='maps')],
            [InlineKeyboardButton("Chart", callback_data='chart_site'),
            InlineKeyboardButton("Summary", callback_data='summarize')],
            [InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"What do you want to know about {user_state[user]['site_name']}?", reply_markup=reply_markup)


    elif query.data == 'start':
        user_state[user]['menu'] = 'start'
        user_state[user]['context'] = "null"
        user_state[user]['site_name'] = None
        await query.message.reply_text("Please type directly the site name you want to know, or like this :\n@ioh_site_bot <site name>.")

    elif query.data == 'data_profil':
        formatted_text = process_data(user_state[user]['context'], return_type='profile')
        await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'data_statistik':
        formatted_text = process_data(user_state[user]['context'], return_type='statistical')
        await query.message.reply_text(formatted_text, parse_mode=ParseMode.HTML)
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu'),
           InlineKeyboardButton("Back to Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'availability':
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'eut':
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'traffic_gb':
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)

    elif query.data == 'dl_prb':
        await query.message.reply_text("This feature is still coming soon")
        keyboard = [
          [InlineKeyboardButton("Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)
