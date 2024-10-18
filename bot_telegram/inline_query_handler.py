from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, ContextTypes, filters
from datetime import datetime, timezone
import logging
import pytz

async def inline_query_handler(update: Update, context):
    # Ambil user_id dari update
    from main import user_state
    user = update.inline_query.from_user.id
    query = update.inline_query.query
    print(f"Received inline query: {query}")  # Debugging line

    results = []

    if query and 'df' in user_state[user]:
        df = user_state[user]['df']

        matching_sites = df[df['site_name'].str.lower().str.contains(query.lower())]

        for index, row in matching_sites.iterrows():
            results.append(
                InlineQueryResultArticle(
                    id=str(row['site_name']),  # Pastikan id unik
                    title=row['site_name'],     # Tampilkan nama situs
                    input_message_content=InputTextMessageContent(row['site_name'])  # Konten pesan
                )
            )

    now = datetime.now(timezone.utc)
    formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")

    # Menggunakan logging dengan timestamp yang telah diformat
    logging.info(f"Received inline query at {formatted_time}: {update.inline_query.query}")

    # Menggunakan print dengan timestamp yang telah diformat
    print(f"Received inline query at {formatted_time}: {update.inline_query.query}")
    await update.inline_query.answer(results, is_personal=True)
