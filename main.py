# Import library yang diperlukan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, filters, ContextTypes
import logging
from bot_telegram.button_handlers import button
from bot_telegram.commands import end,start
from bot_telegram.inline_query_handler import inline_query_handler
from bot_telegram.message_handler import handle_message
from utils import error_handler


# Inisialisasi logger
logger = logging.getLogger(__name__)

# Deklarasi variabel global
user_state = {}
authorized_users = set()
PASSWORD_1 = "ioh"
PASSWORD_2 = "indosat"

def main():
    application = ApplicationBuilder().token("7154493270:AAHXtN0-1H5pvPYK-eRHaIes7m0uhvFU72I").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(InlineQueryHandler(inline_query_handler))  # Menambahkan handler untuk inline query
    application.add_handler(CommandHandler("end", end))  # Pastikan end didefinisikan
    application.add_error_handler(error_handler)  # Add this line to register the error handler


    logger.info("Bot is polling...")
    application.run_polling()


if __name__ == '__main__': # Removed extra underscore from __main_
    main()