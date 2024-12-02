
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
        data = cursor.fetchone()  # Mengambil hanya satu baris

        if data:
            formatted_data = (
                f"enodeb_id: {data[0]}; "
                f"site_id: {data[1]}; "
                f"mc: {data[2]}; "
                f"site_name: temp_{data[3]}; "
                f"tac: {data[4]}; "
                f"region: {data[5]}; "
                f"kabupaten: temp_{data[6]}; "
                f"antenna_height: temp_{data[7]}; "
                f"ran_config: {data[8]}; "
                f"coordinate: {data[9]}; "
                f"azimuth: {data[10]}; "
                f"hostname: temp_{data[11]}; "
                f"transport: {data[12]}; "
                f"site_class: temp_{data[13]}; "
                f"field_type: temp_{data[14]}; "
                f"hub_type: temp_{data[15]}; "
                f"traffic_3id: {data[16]}; "
                f"traffic_im3: {data[17]}; "
                f"total_traffic_gb: {data[18]}; "
                f"category: temp_{data[19]}; "
                f"number_cell_congested: temp_{data[20]}; "
                f"prb: temp_{data[21]}; "
                f"eut: temp_{data[22]}; "
                f"recti_qty: {data[23]}; "
                f"battery_bank: {data[24]}; "
                f"backup_category: temp_{data[25]}; "
                f"pln_cap: temp_{data[26]}; "
                f"billing_pln: cur_{data[27]}; "
                f"unrelated : data not found;"
                f"vlr_subs_3id: {data[28]}; "
                f"vlr_subs_im3: {data[29]}; "
                f"vlr_subs_ioh: {data[30]}; "
                f"rev_ioh: {data[31]}; "
                f"rev_im3: {data[32]}; "
                f"rev_3id: {data[33]}; "
                f"tp : tlp;"
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