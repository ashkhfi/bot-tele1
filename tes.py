import psycopg2
def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            user="postgres",  # Ganti dengan username PostgreSQL
            password="Solo987@!",  # Ganti dengan password PostgreSQL
            host="1.tcp.ap.ngrok.io",  # Ganti dengan host yang benar
            port="21674",  # Ganti dengan port yang benar
            database="npmcj"  # Ganti dengan nama database
        )
        return conn
    except Exception as e:
        print(f"Gagal terhubung ke database: {e}")
        return None


conn = connect_to_postgres()
def execute_query(conn, query, params=None):
    """Eksekusi query SQL dan kembalikan hasilnya."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:  # Jika query menghasilkan hasil (SELECT)
                return cursor.fetchall()
            else:
                conn.commit()  # Jika bukan SELECT, commit perubahan
    except Exception as e:
        print(f"Error saat mengeksekusi query: {e}")

    
if conn:
        # Contoh query untuk mengambil data
      select_query = "SELECT * FROM magang_dataset;"  # Ganti dengan nama tabel Anda
      results = execute_query(conn, select_query)
        
      if results:
          for row in results:
              print(row)  # Cetak hasilnya
        
        # Jangan lupa menutup koneksi
      conn.close()
      print("Koneksi ke database ditutup.")