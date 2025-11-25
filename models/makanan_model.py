from models.database import get_connection

def get_all_makanan():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nama_makanan, harga_default, nama_gambar FROM makanan")
    rows = cur.fetchall()
    conn.close()
    return rows
