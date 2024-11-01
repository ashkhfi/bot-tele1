from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from datetime import datetime, timezone
import logging

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ambil user_id dari update
    from main import user_state
    user = update.inline_query.from_user.id
    query = update.inline_query.query
    print(f"Received inline query: {query}")  # Debugging line

    results = []
    # Memastikan query mengandung kata 'site'
    if 'site' in query.lower():
        # Mengambil bagian query setelah kata 'site'
        search_query = query.lower().split('site', 1)[1].strip()

        if user in user_state and 'df' in user_state[user]:
            df = user_state[user]['df']
            matching_sites = df[df['site_name'].str.lower().str.contains(search_query)]

            for index, row in matching_sites.iterrows():
                results.append(
                    InlineQueryResultArticle(
                        id=str(row['site_name']),  # Pastikan id unik
                        title=(row['site_name']),     # Tampilkan nama situs
                        description=(row['site_id']),
                        input_message_content=InputTextMessageContent(row['site_name']),
                        thumbnail_url='https://firebasestorage.googleapis.com/v0/b/point-of-sale-3639a.appspot.com/o/site.png?alt=media&token=882c52e2-b574-4046-9fc1-4c3f272d9a70',
                        thumbnail_width=512,  
                        thumbnail_height=512 

                    )
                )

    if 'id' in query.lower():
        # Mengambil bagian query setelah kata 'site'
        search_query = query.lower().split('id', 1)[1].strip()

        if user in user_state and 'df' in user_state[user]:
            df = user_state[user]['df']
            matching_sites = df[df['site_id'].str.lower().str.contains(search_query)]

            for index, row in matching_sites.iterrows():
                results.append(
                    InlineQueryResultArticle(
                        id=str(row['site_id']),  # Pastikan id unik
                        title=(row['site_id']),     # Tampilkan nama situs
                        description=(row['site_name']),
                        input_message_content=InputTextMessageContent(row['site_name']),
                        thumbnail_url='https://firebasestorage.googleapis.com/v0/b/point-of-sale-3639a.appspot.com/o/site.png?alt=media&token=882c52e2-b574-4046-9fc1-4c3f272d9a70',
                        thumbnail_width=512,  
                        thumbnail_height=512 

                    )
                )

    now = datetime.now(timezone.utc)
    formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")

    # Menggunakan logging dengan timestamp yang telah diformat
    logging.info(f"Received inline query at {formatted_time}: {update.inline_query.query}")

    # Menggunakan print dengan timestamp yang telah diformat
    print(f"Received inline query at {formatted_time}: {update.inline_query.query}")
    
    # Kirim hasil jika ada
    if results:
        await update.inline_query.answer(results)
    else:
        await update.inline_query.answer([])  # Kirim hasil kosong jika tidak ada yang cocok
