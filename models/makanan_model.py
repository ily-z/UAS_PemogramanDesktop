from models.database import get_connection

def get_all_makanan():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_makanan, nama_makanan,kategori, harga_default, nama_gambar FROM makanan")
    rows = cur.fetchall()
    conn.close()
    return rows
