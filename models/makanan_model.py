from models.database import get_connection

def get_all_makanan():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_makanan, nama_makanan,kategori, harga_default, nama_gambar FROM makanan")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_makanan(nama, harga, kategori, gambar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO makanan (nama_makanan, harga_default, kategori, nama_gambar) VALUES (?, ?, ?, ?)",
                   (nama, harga, kategori, gambar))
    conn.commit()
    conn.close()

def update_makanan(id_makanan, nama, harga, kategori, gambar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE makanan SET nama_makanan=?, harga_default=?, kategori=?, nama_gambar=? WHERE id_makanan=?",
                   (nama, harga, kategori, gambar, id_makanan))
    conn.commit()
    conn.close()

def delete_makanan(id_makanan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM makanan WHERE id_makanan=?", (id_makanan,))
    conn.commit()
    conn.close()
    
def get_makanan_by_id(id_makanan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM makanan WHERE id_makanan=?", (id_makanan,))
    row = cursor.fetchone()
    conn.close()
    return row
