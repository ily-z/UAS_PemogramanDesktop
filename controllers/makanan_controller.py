from models.database import get_connection
from models.makanan_model import get_all_makanan

def load_makanan():
    return get_all_makanan()

def delete_makanan(id_makanan):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM makanan WHERE id_makanan = ?", (id_makanan,))
    conn.commit()
    conn.close()

def insert_makanan(nama_makanan, harga_default, kategori, nama_gambar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO makanan (nama_makanan, harga_default, kategori, nama_gambar)
        VALUES (?, ?, ?, ?)
    """, (nama_makanan, harga_default, kategori, nama_gambar))
    conn.commit()
    conn.close()

def update_makanan(id_makanan, nama_makanan, harga_default, kategori, nama_gambar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE makanan
        SET nama_makanan = ?, harga_default = ?, kategori = ?, nama_gambar = ?
        WHERE id_makanan = ?
    """, (nama_makanan, harga_default, kategori, nama_gambar, id_makanan))
    conn.commit()
    conn.close()