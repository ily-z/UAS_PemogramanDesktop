from models.database import get_connection
from datetime import datetime
import sqlite3

def insert_transaksi(detail_items, total, id_pembeli=None, id_kasir=None, id_voucher=None):
    """
    Simpan transaksi dan detail_transaksi ke database

    - Tabel transaksi: (id_transaksi, tgl_transaksi, id_pembeli, id_kasir, id_voucher, total)
    - Tabel detail_transaksi: (id_detail, id_transaksi, id_makanan, kuantitas, harga_satuan, subtotal)

    Args:
        detail_items: list of dict {id_makanan, nama_makanan, harga_satuan, kuantitas, diskon_pct, subtotal}
        total: numeric total transaksi (sudah termasuk diskon per item)
        id_pembeli, id_kasir, id_voucher: optional IDs dari database
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Deteksi style placeholder: sqlite uses "?", MySQLdb / pymysql use "%s"
    use_qmark = False
    try:
        if isinstance(conn, sqlite3.Connection):
            use_qmark = True
    except Exception:
        use_qmark = False

    ph = "?" if use_qmark else "%s"

    try:
        # 1) Insert transaksi
        tgl_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_val = int(total) if total is not None else 0

        placeholders = ", ".join([ph]*5)
        query_transaksi = f"INSERT INTO transaksi (tgl_transaksi, id_pembeli, id_kasir, id_voucher, total) VALUES ({placeholders})"
        params_transaksi = (tgl_transaksi, id_pembeli, id_kasir, id_voucher, total_val)

        print("DEBUG: query_transaksi:", query_transaksi)
        print("DEBUG: params_transaksi:", params_transaksi)
        cursor.execute(query_transaksi, params_transaksi)

        # Ambil id_transaksi yang baru dibuat
        id_transaksi = cursor.lastrowid
        print("DEBUG: id_transaksi:", id_transaksi)

        # 2) Insert setiap detail item
        placeholders_detail = ", ".join([ph]*5)
        query_detail = f"INSERT INTO detail_transaksi (id_transaksi, id_makanan, kuantitas, harga_satuan, subtotal) VALUES ({placeholders_detail})"

        for idx, item in enumerate(detail_items):
            params_detail = (
                id_transaksi,
                int(item["id_makanan"]),
                int(item["kuantitas"]),
                int(item["harga_satuan"]),
                int(item["subtotal"])
            )
            print(f"DEBUG: detail {idx} params:", params_detail)
            cursor.execute(query_detail, params_detail)

        conn.commit()
        print(f"✓ Transaksi #{id_transaksi} berhasil disimpan dengan {len(detail_items)} item")

    except Exception as e:
        conn.rollback()
        print("ERROR:", str(e))
        raise Exception(f"Gagal menyimpan transaksi: {str(e)}")

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass