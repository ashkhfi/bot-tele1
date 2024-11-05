import math

from telegram import Update
from telegram.ext import ContextTypes

# Fungsi untuk menghitung jarak menggunakan rumus Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius Bumi dalam kilometer
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Fungsi untuk menghitung bearing
def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(x, y))
    bearing = (bearing + 360) % 360
    return bearing

# Fungsi untuk mendapatkan arah mata angin dengan emoji
def get_compass_direction_with_emoji(bearing):
    directions = [
        ("North", "⬆️"), 
        ("Northeast", "↗️"), 
        ("East", "➡️"), 
        ("Southeast", "↘️"), 
        ("South", "⬇️"), 
        ("Southwest", "↙️"), 
        ("West", "⬅️"), 
        ("Northwest", "↖️")
    ]

    index = round(bearing / 45) % 8
    return directions[index]

def parse_coordinates(coordinate):
    lat, lon = map(float, coordinate.split(','))
    return lat, lon

async def find_nearest_locations(update: Update, context: ContextTypes.DEFAULT_TYPE, lat: float, lon: float) -> None:
    from config import connect_to_postgres
    from utils import get_site_name

    # Gunakan lat dan lon dari parameter yang diterima
    current_location = {'latitude': lat, 'longitude': lon}
    conn = connect_to_postgres()

    if conn:
        df_site_name = get_site_name(conn)
        if df_site_name is not None and not df_site_name.empty:
            locations = [
                {
                    'name': row['site_name'],
                    'site_id': row['site_id'],
                    'latitude': parse_coordinates(row['coordinate'])[0],
                    'longitude': parse_coordinates(row['coordinate'])[1]
                }
                for _, row in df_site_name.iterrows()
            ]

            # Hitung jarak dan arah untuk semua lokasi
            distances = []
            for location in locations:
                distance = haversine(current_location['latitude'], current_location['longitude'], location['latitude'], location['longitude'])
                bearing = calculate_bearing(current_location['latitude'], current_location['longitude'], location['latitude'], location['longitude'])
                direction, emoji = get_compass_direction_with_emoji(bearing)
                distances.append((distance, location, bearing, direction, emoji))

            # Urutkan berdasarkan jarak dan ambil 10 lokasi terdekat
            distances.sort(key=lambda x: x[0])
            top_nearest_locations = distances[:5]

            # Buat pesan hasil
            message = "*5 Nearest Sites:*\n\n"
            for distance, location, bearing, direction, emoji in top_nearest_locations:
                distance_text = f"{distance * 1000:.0f} m" if distance < 1 else f"{distance:.2f} KM"
                message += (
                    f" • `{location['name']}`\n"
                    f"    ‣ Site ID: `{location['site_id']}`\n"
                    f"    ‣ Distance: {distance_text}\n"
                    f"    ‣ Bearing: {bearing:.0f}°\n"
                    f"    ‣ Direction: {direction}\\({emoji}\\)\n\n"  # Escape parentheses
                )

            # Add a note at the bottom, escaping special characters
            message += "***Note: Tap on the Site Name or Site ID above to copy them to your clipboard\\.***"


            await update.message.reply_text(message, parse_mode="MarkdownV2")
        else:
            await update.message.reply_text("Location Data Not Found.")
        conn.close()
    else:
        await update.message.reply_text("Failed to connect database")