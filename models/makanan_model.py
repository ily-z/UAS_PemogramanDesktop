# ...existing code...
from models.database import get_connection

def get_all_makanan():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_makanan, nama_makanan, harga_default, kategori, nama_gambar FROM makanan")
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
# ...existing code...
class MakananModel:
    def _init_(self):
        self._conn = get_connection()
        self._cur = self._conn.cursor()
        # Buat tabel dengan kolom yang dipakai oleh controller/view
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS makanan (
                id_makanan INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_makanan TEXT NOT NULL,
                harga_default INTEGER NOT NULL,
                kategori TEXT,
                nama_gambar TEXT
            );
        """)
        self._conn.commit()

    def get_all(self):
        self._cur.execute("SELECT id_makanan, nama_makanan, harga_default, kategori, nama_gambar FROM makanan ORDER BY id_makanan DESC")
        return self._cur.fetchall()

    def insert(self, name, price, kategori, nama_gambar=None):
        self._cur.execute(
            "INSERT INTO makanan (nama_makanan, harga_default, kategori, nama_gambar) VALUES (?, ?, ?, ?)",
            (name, price, kategori, nama_gambar)
        )
        self._conn.commit()
        return self._cur.lastrowid

    def update(self, id_, name, price, kategori=None, nama_gambar=None):
        self._cur.execute(
            "UPDATE makanan SET nama_makanan=?, harga_default=?, kategori=?, nama_gambar=? WHERE id_makanan=?",
            (name, price, kategori, nama_gambar, id_)
        )
        self._conn.commit()

    def delete(self, id_):
        self.cur.execute("DELETE FROM makanan WHERE id_makanan=?", (id,))
        self._conn.commit()

    def close(self):
        self._conn.close()
# ...existing code...
