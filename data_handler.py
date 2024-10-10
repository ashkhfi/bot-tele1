
from config import connect_to_postgres

def set_context(conn, site_name):
    query = f"""
    SELECT *
    FROM magang_dataset
    WHERE site_name = '{site_name}';
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
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
            )
        else:
            formatted_data = "null"

        return formatted_data

    except Exception as e:
        return f"error: {str(e)}"


