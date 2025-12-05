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



import sqlite3
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "..", "pemesanan_makanan.db")  # relatif ke repo root

class MakananModel:
    def __init__(self):
        self._conn = sqlite3.connect(DB_PATH)
        self._cur = self._conn.cursor()
        # jika tabel belum ada, buat (idempotent)
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS makanan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            );
        """)
        self._conn.commit()

    def get_all(self):
        self._cur.execute("SELECT * FROM makanan ORDER BY id_makanan DESC")
        return self._cur.fetchall()

    def insert(self, name, category,price):
        self._cur.execute("INSERT INTO makanan (nama_makanan, harga_default, kategori) VALUES (?, ?, ?)", (name, category,price))
        self._conn.commit()
        return self._cur.lastrowid

    def update(self, id_, name, price):
        self._cur.execute("UPDATE makanan SET nama_makanan=?, harga_default=? WHERE id_makanan=?", (name, price, id_))
        self._conn.commit()

    def delete(self, id_):
        self._cur.execute("DELETE FROM makanan WHERE id_makanan=?", (id_,))
        self._conn.commit()

    def close(self):
        self._conn.close()
