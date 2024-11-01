import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy as np


def plot_data(df, data, title):
    # Konversi kolom 'date' ke format datetime
    df['date'] = pd.to_datetime(df['date'])

    # Mengurutkan DataFrame berdasarkan 'date'
    df = df.sort_values('date')

    # Plot line chart untuk setiap sector_id_hos
    plt.figure(figsize=(12, 6))

    # Mendapatkan daftar unik dari sector_id_hos
    sector_ids = df['sector_id_hos'].unique()

    # Loop untuk setiap sector_id_hos
    for sector_id_hos in sector_ids:
        # Filter DataFrame untuk setiap sector_id_hos
        filtered_df = df[df['sector_id_hos'] == sector_id_hos]

        # Buat array untuk interpolasi
        x = filtered_df['date'].map(pd.Timestamp.timestamp)  # Konversi ke timestamp
        y = filtered_df[f'{data}'].values

        # Menggunakan B-Spline untuk interpolasi
        spline = make_interp_spline(x, y, k=3)  # k=3 untuk cubic spline
        x_new = np.linspace(x.min(), x.max(), 300)  # 300 titik baru untuk kehalusan
        y_new = spline(x_new)

        # Plot data untuk sector_id_hos dengan nilai interpolasi
        plt.plot(pd.to_datetime(x_new, unit='s'), y_new, label=sector_id_hos, linewidth=2)

    # Menambahkan judul dan label
    plt.title(f'{title}')
    plt.xlabel('Date')
    plt.ylabel('value')
    plt.xticks(rotation=45)  # Memutar label tanggal untuk keterbacaan
    plt.legend(title='Sector ID HOS', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid()

    # Tampilkan grafik
    plt.tight_layout()
    

    # Simpan grafik sebagai PNG
    plt.savefig(f"chart.jpg", format='jpg', dpi=200)  # Simpan sebagai file PNG


# Contoh pemanggilan fungsi
# plot_data(df, 'data_column_name', 'Chart Title', 'output_filename')
