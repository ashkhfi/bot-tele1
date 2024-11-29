
from config import connect_to_postgres

def set_context(conn, site_name):
    query = """
    SELECT *
    FROM magang_dataset
    WHERE site_name ILIKE %s;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (site_name,))
        row = cursor.fetchone()  # Mengambil hanya satu baris

        if row:
            formatted_data = (
            f"enodeb_id: {row['enodeb_id']}; site_id: {row['site_id']}; mc: {row['mc']}; region: {row['region']}; "
            f"regency: temp_{row['kabupaten']}; coordinate: {row['coordinate']}; tac: {row['tac']}; "
            f"antenna_height: temp_{row['antenna_height']}; hostname: temp_{row['hostname']}; site_class: temp_{row['site_class']}; "
            f"transport: temp_{row['transport']}; azimuth: {row['azimuth']}; hub_type: temp_{row['hub_type']}; "
            f"field_type: temp_{row['field_type']}; category: temp_{row['category']}; "
            f"number_cell_congested: temp_{row['number_cell_congested']}; site_name: temp_{row['site_name']}; "
            f"traffic_3id: {row['traffic_3id']}; traffic_im3: {row['traffic_im3']}; total_traffic_gb: {row['total_traffic_gb']}; "
            f"prb: temp_{row['prb']}; eut: temp_{row['eut']}; ran_config: temp_{row['ran_config']}; unrelated : data not found; "
            f"recti_qty: temp_{row['recti_qty']}; battery_bank: temp_{row['battery_bank']}; backup_category: temp_{row['backup_category']}; "
            f"pln_cap: temp_{row['pln_cap']}; billing_pln: cur_{row['billing_pln']}; "
            f"vlr_subs_3id: {row['vlr_subs_3id']}; vlr_subs_im3: {row['vlr_subs_im3']}; vlr_subs_ioh: {row['vlr_subs_ioh']}; "
            f"rev_ioh: {row['rev_ioh']}; rev_im3: {row['rev_im3']}; rev_3id: {row['rev_3id']}; tp : tlp;"
        )
        else:
            formatted_data = "null"

        return formatted_data

    except Exception as e:
        return f"error: {str(e)}"



import pandas as pd

def get_data_chart(conn, site_name, interval ):
    cursor = conn.cursor()
    sitename = site_name.upper()

    sql = f"""
    SELECT *
    FROM magang_datachart
    WHERE DATE(date) >= (
          SELECT MAX(date) 
          FROM magang_datachart 
          WHERE enodeb_name = '{sitename}'
        ) - INTERVAL '{interval} days'
      AND DATE(date) <= (
          SELECT MAX(date) 
          FROM magang_datachart 
          WHERE enodeb_name = '{sitename}'
        )
      AND enodeb_name = '{sitename}'
    ORDER BY date DESC;
"""



    try:
        # Menjalankan query dengan parameter
        cursor.execute(sql, (site_name,))

        # Mengambil hasil
        results = cursor.fetchall()

        # Mengambil nama kolom
        columns = [desc[0] for desc in cursor.description]

        # Mengonversi hasil menjadi DataFrame
        df = pd.DataFrame(results, columns=columns)

        return df
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')
        return pd.DataFrame()
    finally:
        # Menutup cursor
        cursor.close()

def get_data_sumarize(conn, site_name ):
    # Membuat objek cursor dari koneksi
    cursor = conn.cursor()

    # Query untuk mendapatkan satu data per tanggal berdasarkan enodeb_name
    sitename = site_name.upper()

    sql = f"""
        WITH latest_date AS (
            SELECT MAX(date) AS date
            FROM magang_datachart
            WHERE enodeb_name = '{sitename}'
        )
        SELECT *
        FROM magang_datachart
        WHERE date = (SELECT date FROM latest_date)
        AND enodeb_name = '{sitename}';
    """
    try:
        # Menjalankan query dengan parameter
        cursor.execute(sql, (site_name,))

        # Mengambil hasil
        results = cursor.fetchall()

        # Mengambil nama kolom
        columns = [desc[0] for desc in cursor.description]

        # Mengonversi hasil menjadi DataFrame
        df = pd.DataFrame(results, columns=columns)

        return df
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')
        return pd.DataFrame()
    finally:
        # Menutup cursor
        cursor.close()