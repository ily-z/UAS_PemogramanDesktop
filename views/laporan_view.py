from PyQt6 import QtWidgets, QtCore
from models.database import get_connection
import sqlite3


def load_transaksi():
    """Load semua transaksi dari database"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                t.id_transaksi,
                t.tgl_transaksi,
                p.nama_pembeli,
                k.nama_kasir,
                COALESCE(v.nama_voucher, '-') as nama_voucher,
                t.total
            FROM transaksi t
            LEFT JOIN pembeli p ON t.id_pembeli = p.id_pembeli
            LEFT JOIN kasir k ON t.id_kasir = k.id_kasir
            LEFT JOIN diskon_voucher v ON t.id_voucher = v.id_voucher
            ORDER BY t.tgl_transaksi DESC
        """)
        
        rows = cursor.fetchall()
        result = []
        for r in rows:
            if isinstance(r, sqlite3.Row):
                result.append(dict(r))
            else:
                result.append({
                    "id_transaksi": r[0],
                    "tgl_transaksi": r[1],
                    "nama_pembeli": r[2],
                    "nama_kasir": r[3],
                    "nama_voucher": r[4],
                    "total": r[5]
                })
        return result
    except Exception as e:
        print(f"Error load transaksi: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def load_detail_transaksi(id_transaksi):
    """Load detail transaksi berdasarkan id_transaksi"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                dt.id_detail,
                dt.id_makanan,
                m.nama_makanan,
                dt.kuantitas,
                dt.harga_satuan,
                dt.subtotal
            FROM detail_transaksi dt
            LEFT JOIN makanan m ON dt.id_makanan = m.id_makanan
            WHERE dt.id_transaksi = ?
            ORDER BY dt.id_detail ASC
        """, (id_transaksi,))
        
        rows = cursor.fetchall()
        result = []
        for r in rows:
            if isinstance(r, sqlite3.Row):
                result.append(dict(r))
            else:
                result.append({
                    "id_detail": r[0],
                    "id_makanan": r[1],
                    "nama_makanan": r[2],
                    "kuantitas": r[3],
                    "harga_satuan": r[4],
                    "subtotal": r[5]
                })
        return result
    except Exception as e:
        print(f"Error load detail transaksi: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


class LaporanView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Laporan Transaksi")
        self.resize(900, 600)
        
        mainLayout = QtWidgets.QVBoxLayout(self)
        
        # ===== HEADER =====
        headerLabel = QtWidgets.QLabel("Riwayat Transaksi")
        headerLabel.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        mainLayout.addWidget(headerLabel)
        
        # ===== TABEL TRANSAKSI =====
        self.tabelTransaksi = QtWidgets.QTableWidget()
        self.tabelTransaksi.setColumnCount(7)
        self.tabelTransaksi.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Pembeli", "Kasir", "Voucher", "Total (Rp)", "Detail"
        ])
        self.tabelTransaksi.setColumnWidth(0, 50)
        self.tabelTransaksi.setColumnWidth(1, 150)
        self.tabelTransaksi.setColumnWidth(2, 120)
        self.tabelTransaksi.setColumnWidth(3, 120)
        self.tabelTransaksi.setColumnWidth(4, 120)
        self.tabelTransaksi.setColumnWidth(5, 120)
        self.tabelTransaksi.setColumnWidth(6, 100)
        
        mainLayout.addWidget(self.tabelTransaksi)
        
        # ===== LOAD DATA =====
        self.loadDataTransaksi()
        
        self.setLayout(mainLayout)
    
    def loadDataTransaksi(self):
        """Load dan tampilkan data transaksi di tabel"""
        data = load_transaksi()
        self.tabelTransaksi.setRowCount(0)
        
        for transaksi in data:
            row = self.tabelTransaksi.rowCount()
            self.tabelTransaksi.insertRow(row)
            
            # Kolom: ID, Tanggal, Pembeli, Kasir, Voucher, Total
            self.tabelTransaksi.setItem(row, 0, QtWidgets.QTableWidgetItem(str(transaksi["id_transaksi"])))
            self.tabelTransaksi.setItem(row, 1, QtWidgets.QTableWidgetItem(transaksi["tgl_transaksi"]))
            self.tabelTransaksi.setItem(row, 2, QtWidgets.QTableWidgetItem(transaksi["nama_pembeli"]))
            self.tabelTransaksi.setItem(row, 3, QtWidgets.QTableWidgetItem(transaksi["nama_kasir"]))
            self.tabelTransaksi.setItem(row, 4, QtWidgets.QTableWidgetItem(transaksi["nama_voucher"]))
            self.tabelTransaksi.setItem(row, 5, QtWidgets.QTableWidgetItem(f"Rp {transaksi['total']:,}"))
            
            # Tombol Detail
            btnDetail = QtWidgets.QPushButton("Lihat Detail")
            btnDetail.setStyleSheet("background-color: #2196F3; color: white;")
            btnDetail.clicked.connect(
                lambda checked, tid=transaksi["id_transaksi"]: self.lihatDetail(tid)
            )
            self.tabelTransaksi.setCellWidget(row, 6, btnDetail)
    
    def lihatDetail(self, id_transaksi):
        """Tampilkan detail transaksi dalam dialog"""
        detail_items = load_detail_transaksi(id_transaksi)
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Detail Transaksi #{id_transaksi}")
        dialog.resize(600, 400)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Header
        headerLabel = QtWidgets.QLabel(f"Transaksi #{id_transaksi}")
        headerLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(headerLabel)
        
        # Tabel detail
        tabelDetail = QtWidgets.QTableWidget()
        tabelDetail.setColumnCount(5)
        tabelDetail.setHorizontalHeaderLabels([
            "Nama Makanan", "Kuantitas", "Harga Satuan", "Subtotal", ""
        ])
        tabelDetail.setColumnWidth(0, 180)
        tabelDetail.setColumnWidth(1, 80)
        tabelDetail.setColumnWidth(2, 100)
        tabelDetail.setColumnWidth(3, 120)
        
        for detail in detail_items:
            row = tabelDetail.rowCount()
            tabelDetail.insertRow(row)
            
            tabelDetail.setItem(row, 0, QtWidgets.QTableWidgetItem(detail.get("nama_makanan", "N/A")))
            tabelDetail.setItem(row, 1, QtWidgets.QTableWidgetItem(str(detail["kuantitas"])))
            tabelDetail.setItem(row, 2, QtWidgets.QTableWidgetItem(f"Rp {detail['harga_satuan']:,}"))
            tabelDetail.setItem(row, 3, QtWidgets.QTableWidgetItem(f"Rp {detail['subtotal']:,}"))
        
        layout.addWidget(tabelDetail)
        
        # Total
        if detail_items:
            total = sum([item["subtotal"] for item in detail_items])
            totalLabel = QtWidgets.QLabel(f"Total: Rp {total:,}")
            totalLabel.setStyleSheet("font-size: 12px; font-weight: bold; text-align: right;")
            layout.addWidget(totalLabel)
        
        # Tombol Tutup
        btnTutup = QtWidgets.QPushButton("Tutup")
        btnTutup.clicked.connect(dialog.close)
        layout.addWidget(btnTutup)
        
        dialog.exec()
