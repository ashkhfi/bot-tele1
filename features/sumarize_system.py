import pandas as pd

def generate_summary_report(df):
    # 1. Site Availability
    avg_site_availability = df['availability'].mean()
    if avg_site_availability > 99.75:
        site_availability_label = "Availability Good"
    elif 99.00 <= avg_site_availability <= 99.7:
        site_availability_label = "Availability Fair"
    else:
        site_availability_label = "Availability Not Good"

    # 2. Sector Availability
    days_below_99_7_site = df[df['availability'] < 99.7]['date'].nunique()
    dates_below_99_7_site = df[df['availability'] < 99.7]['date'].unique()
    sectors_below_99 = df[df['availability'] < 99]['sector_id_hos'].unique()
    highest_sector = df.loc[df['availability'].idxmax()]['sector_id_hos']
    lowest_sector = df.loc[df['availability'].idxmin()]['sector_id_hos']

    # 3. Site EUT
    average_eut = df['eut'].mean()
    congested_sectors = df[df['eut'] < 1.4]['sector_id_hos'].unique()
    nearly_congested_sectors = df[(df['eut'] >= 1.4) & (df['eut'] < 2)]['sector_id_hos'].unique()
    not_congested_sectors = df[df['eut'] > 2]['sector_id_hos'].unique()

    # 4. Sector EUT
    highest_eut_sector = df.loc[df['eut'].idxmax()]['sector_id_hos']
    lowest_eut_sector = df.loc[df['eut'].idxmin()]['sector_id_hos']

    # 5. Sector dl_prb
    average_dl_prb = df['dl_prb'].mean()
    loaded_sectors = df[df['dl_prb'] < 93]['sector_id_hos'].unique()
    nearly_loaded_sectors = df[(df['dl_prb'] >= 85) & (df['dl_prb'] < 93)]['sector_id_hos'].unique()
    highest_dl_prb_sector = df.loc[df['dl_prb'].idxmax()]['sector_id_hos']
    lowest_dl_prb_sector = df.loc[df['dl_prb'].idxmin()]['sector_id_hos']

    # 6. Site traffic_gb (per Sector, Averaged over 1 Week)
    traffic_per_sector = df.groupby('sector_id_hos')['traffic_gb'].sum() / 7

    # 7. Sector traffic_gb
    highest_traffic_gb_sector = df.loc[df['traffic_gb'].idxmax()]['sector_id_hos']
    lowest_traffic_gb_sector = df.loc[df['traffic_gb'].idxmin()]['sector_id_hos']

    # Menyiapkan semua output sebagai satu variabel string
    output_summary = f"""
Site Availability:
- Overall Average Availability: {avg_site_availability:.2f}
- Site Availability Label: {site_availability_label}

Number of Days with Availability < 99.7: {days_below_99_7_site}
Dates with Availability < 99.7:
""" + "\n".join(f"  - {date.strftime('%Y-%m-%d')}" for date in dates_below_99_7_site) + f"""

Sector Availability:
- Sector with Highest Availability: {highest_sector}
- Sector with Lowest Availability: {lowest_sector}
- Number of Sectors with Availability < 99: {len(sectors_below_99)}

Site EUT:
- Average EUT: {average_eut:.2f}
- Number of Congested Sectors (EUT < 1.4): {len(congested_sectors)}
- Number of Nearly Congested Sectors (EUT 1.4-2): {len(nearly_congested_sectors)}
- Number of Not Congested Sectors (EUT > 2): {len(not_congested_sectors)}

Sector EUT:
- Highest EUT Sector: {highest_eut_sector}
- Lowest EUT Sector: {lowest_eut_sector}

Sector PRB:
- Average PRB: {average_dl_prb:.2f}
- Number of Loaded Sectors (PRB < 93%): {len(loaded_sectors)}
- Number of Nearly Loaded Sectors (PRB 85-93%): {len(nearly_loaded_sectors)}
- Sector with Highest PRB Usage: {highest_dl_prb_sector}
- Sector with Lowest PRB Usage: {lowest_dl_prb_sector}

Site Traffic (GB per Sector, Averaged over 1 Week):
""" + "\n".join(f"- Sector {sector}: {traffic:.2f} GB" for sector, traffic in traffic_per_sector.items()) + f"""

Sector Traffic:
- Sector with Highest Traffic: {highest_traffic_gb_sector}
- Sector with Lowest Traffic: {lowest_traffic_gb_sector}
"""

    # Mengembalikan seluruh output dalam satu variabel
    return output_summary

# Contoh penggunaan fungsi dengan dataframe df_7
# print(generate_summary_report(df_7))
