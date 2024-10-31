import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

def log_to_spreadsheet(user, question, answer):
    try:
        # Tentukan scope untuk Google Sheets dan Google Drive API
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        # Autentikasi client menggunakan credential dari file JSON yang diberikan
        creds = ServiceAccountCredentials.from_json_keyfile_name('tubes-iot-407403-c1d3677c0f9f.json', scope)
        client = gspread.authorize(creds)

        try:
            # Coba buka spreadsheet berdasarkan nama
            spreadsheet = client.open('log user')
            print(f"Spreadsheet 'log user' ditemukan.")
        except gspread.SpreadsheetNotFound:
            # Jika spreadsheet tidak ditemukan, buat spreadsheet baru
            spreadsheet = client.create('log user')
            print(f"Spreadsheet baru '{'log user'}' berhasil dibuat.")
            # Bagikan spreadsheet ke akun email yang digunakan untuk kolaborasi
            spreadsheet.share(spreadsheet.client.auth.client_email, perm_type='user', role='writer')
            print("Izin telah diberikan kepada email service account.")

        # Menampilkan link spreadsheet
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        print(f"Spreadsheet URL: {spreadsheet_url}")

        # Pilih worksheet (misalnya sheet pertama)
        worksheet = spreadsheet.sheet1

        # Ambil tanggal saat ini
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log data pengguna, tanggal, pertanyaan, dan jawaban
        log_data = [user, current_date, question, answer]

        # Tulis data ke worksheet (append row)
        worksheet.append_row(log_data)

        print("Data berhasil disimpan ke Google Sheets!")
        
    except gspread.exceptions.APIError as api_error:
        print(f"Terjadi kesalahan API: {api_error}")
    except gspread.exceptions.GSpreadException as gspread_error:
        print(f"Kesalahan GSpread: {gspread_error}")
    except FileNotFoundError:
        print("File kredensial tidak ditemukan. Pastikan path ke file JSON sudah benar.")
    except Exception as e:
        print(f"Kesalahan lain terjadi: {str(e)}")  # Memastikan detail kesalahan ditampilkan

# Contoh pemanggilan fungsi
log_to_spreadsheet("test_user", "aaaaaaaaaaa", "bbbbbbbbbbbb")
