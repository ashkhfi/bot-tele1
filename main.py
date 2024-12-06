# Import library yang diperlukan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, filters, ContextTypes
import logging
from bot_telegram.button_handlers import button
from bot_telegram.commands import site,start, near, receive_location, help
from bot_telegram.inline_query_handler import inline_query_handler
from bot_telegram.message_handler import handle_message
import sys
sys.stdout.reconfigure(encoding='utf-8')





user_state = {}
authorized_users = set()
PASSWORD_1 = "IOH4Indonesia"
PASSWORD_2 = "indosat"
PASSWORD_3 = "Usertest234"

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Exception while handling an update:")


def main():
    try:
        token = '7617596594:AAFyiPhJU4lcaBsbFgdTjdxKPPXV4dHiUqI'
        if not token:
            print("Token bot tidak ditemukan. Pastikan token diatur di variabel lingkungan.")
            return

        application = ApplicationBuilder().token(token).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(InlineQueryHandler(inline_query_handler))
        application.add_handler(CommandHandler("site", site))
        application.add_handler(CommandHandler("near", near))
        application.add_handler(CommandHandler("help", help))
        application.add_handler(MessageHandler(filters.LOCATION | filters.TEXT, receive_location))
        
        # Menambahkan handler untuk error
        application.add_error_handler(error_handler)

        print("Bot is polling...")
        application.run_polling()
    except Exception as e:
        print("Unexpected error in main(): %s", e)



if __name__ == '__main__': 
    main()
