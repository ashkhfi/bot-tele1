from config import connect_to_postgres
from data_handler import get_data_chart, get_data_sumarize
from chart_system import plot_data
from sumarize_system import summarize_issues

conn = connect_to_postgres()
if conn:
    df = get_data_chart(conn, 'lte_tampe_pl', 14)  # Mendapatkan data 7 hari terakhir
    if df.empty:
        print("Tidak ada data yang ditemukan.")
    else:
        print("ada data yang ditemukan.")
        # a = summarize_issues(df)
        # print(a['message'])
else:
    print("Terjadi kesalahan koneksi")
