from config import connect_to_postgres
from data_handler import get_data_chart
from chart_system import plot_data

conn = connect_to_postgres()
if conn:
    df = get_data_chart(conn, 'lte_tampe_pl', 20)  # Mendapatkan data 7 hari terakhir
    if df.empty:
        print("Tidak ada data yang ditemukan.")
    else:
        plot_data(df, 'eut', 'availability')  # Menampilkan chart
else:
    print("Terjadi kesalahan koneksi")
