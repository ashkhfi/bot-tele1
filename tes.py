from config import connect_to_postgres
from data_handler import get_data_sumarize
from chart_system import plot_data
from sumarize_system import summarize_issues

conn = connect_to_postgres()
if conn:
    df = get_data_sumarize(conn, 'lte_tampe_pl')  # Mendapatkan data 7 hari terakhir
    if df.empty:
        print("Tidak ada data yang ditemukan.")
    else:
        a = summarize_issues(df)
        print(a['message'])
else:
    print("Terjadi kesalahan koneksi")
