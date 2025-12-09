from models.database import get_connection

def insert_transaksi(id_makanan, qty, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transaksi (id_makanan, qty, total_harga) VALUES (%s, %s, %s)",
        (id_makanan, qty, total)
    )
    conn.commit()
    conn.close()