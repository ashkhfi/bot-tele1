# Import library yang diperlukan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, filters, ContextTypes
import logging
from bot_telegram.button_handlers import button
from bot_telegram.commands import site,start, near, receive_location
from bot_telegram.inline_query_handler import inline_query_handler
from bot_telegram.message_handler import handle_message
import sys
sys.stdout.reconfigure(encoding='utf-8')


logger = logging.getLogger(__name__)

user_state = {}
authorized_users = set()
PASSWORD_1 = "IOH4Indonesia"
PASSWORD_2 = "indosat"
PASSWORD_3 = "Usertest234"

def main():
    application = ApplicationBuilder().token("7511717176:AAH-HV3_vOkiy3v_6MX7eoE1cmxuRfms_dc").build()
    #7154493270:AAFJAlUOfrJYjgiWHVF_hwAjVOy1jw1a4Js 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(InlineQueryHandler(inline_query_handler))  # Menambahkan handler untuk inline query
    application.add_handler(CommandHandler("site", site))  # Pastikan end didefinisikan
    application.add_handler(CommandHandler("near", near))
    application.add_handler(MessageHandler(filters.LOCATION | filters.TEXT, receive_location))

    logger.info("Bot is polling...")
    application.run_polling()


if __name__ == '__main__': 
    main()
