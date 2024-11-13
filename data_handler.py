
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
                f"site_name: {data[3]}; "
                f"tac: {data[4]}; "
                f"region: {data[5]}; "
                f"kabupaten: {data[6]}; "
                f"antenna_height: {data[7]}; "
                f"ran_config: {data[8]}; "
                f"coordinate: {data[9]}; "
                f"azimuth: {data[10]}; "
                f"hostname: {data[11]}; "
                f"transport: {data[12]}; "
                f"site_class: {data[13]}; "
                f"field_type: {data[14]}; "
                f"hub_type: {data[15]}; "
                f"traffic_3id: {data[16]}; "
                f"traffic_im3: {data[17]}; "
                f"total_traffic_gb: {data[18]}; "
                f"category: {data[19]}; "
                f"number_cell_congested: {data[20]}; "
                f"prb: {data[21]}; "
                f"eut: {data[22]}; "
                f"unrelated : data not found;. "
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