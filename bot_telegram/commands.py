# Import library yang diperlukan
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from features.near_location_site import find_nearest_locations



# Fungsi untuk menangani perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state, authorized_users  # Impor di dalam fungsi
    from config import connect_to_postgres
    from utils import get_site_name
    user = update.effective_user.id  

    if user not in user_state:
        user_state[user] = {
            "context": None,
            "near": False,
            "menu": "start",
            "waiting_for_password": False,
            "site_name": "",
            "site_id": "",
            "df": None
        }

    # Menghubungkan ke database
    conn = connect_to_postgres()

    if conn:
        df = get_site_name(conn)
        if df is not None:
            user_state[user]['df'] = df
            print(df)
        conn.close()
    else:
        await update.message.reply_text("Failed to connect to the database.")


    if user in authorized_users:
        await update.message.reply_text(
            """This is a site data chatbot, First time, you will need to enter the site ID or site name,

To help you find The Right Site , please use search command:
- by siteid : <b>@ioh_site_bot</b><i>[space]</i><b> id </b><i>[space]</i><b> siteid</b>
- by sitename : <b>@ioh_site_bot</b><i>[space]</i><b> site </b><i>[space]</i><b> sitename</b>

Chat is only in english!"""
        ,parse_mode=ParseMode.HTML,reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text("Please enter the password to proceed:")
        user_state[user]["waiting_for_password"] = True

# Fungsi untuk menangani perintah /site
async def site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengakhiri sesi pengguna"""
    from main import user_state  # Impor di dalam fungsi
    from config import connect_to_postgres
    from utils import get_site_name
    user_id = update.effective_user.id
    user_state[user_id]['context'] = None
    user_state[user_id]['near'] = False
    user_state[user_id]['menu'] = 'start'
    user_state[user_id]['waiting_for_password'] = False
    user_state[user_id]['site_name'] = ""
    user_state[user_id]['site_id'] = ""
    user_state[user_id]['df'] = None
   
    await update.message.reply_text(
            """This is a site data chatbot, First time, you will need to enter the site ID or site name,

To help you find The Right Site , please use search command:
- by siteid : <b>@ioh_site_bot</b><i>[space]</i><b> id </b><i>[space]</i><b> siteid</b>
- by sitename : <b>@ioh_site_bot</b><i>[space]</i><b> site </b><i>[space]</i><b> sitename</b>

Chat is only in english!"""
        ,parse_mode=ParseMode.HTML,reply_markup=ReplyKeyboardRemove()
        )
    conn = connect_to_postgres()

    if conn:
        df = get_site_name(conn)
        if df is not None:
            user_state[user_id]['df'] = df
            print(df)
        conn.close()
    else:
        await update.message.reply_text("Failed to connect to the database.")


async def near(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import user_state

    user_id = update.effective_user.id
    user_state[user_id]['near'] = True
    await update.message.reply_text("Please share your location using Telegram's '<b>Share Location</b>' feature,"
            "so we can find the closest place to your location.", parse_mode=ParseMode.HTML)

async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location
 
    from main import user_state 
    user_id = update.effective_user.id
    near = user_state[user_id]['near']
    if(near == True):
        if user_location:
            lat = user_location.latitude
            lon = user_location.longitude
            await update.message.reply_text(
            f"Your location was successfully accepted!")
            await find_nearest_locations(update, context, lat, lon)
            user_state[user_id]['near'] = False

        else:
            await update.message.reply_text("Failed to receive location. Try again by sharing your location.")
    else:
        await update.message.reply_text("Please use /near first to find the nearest site")


