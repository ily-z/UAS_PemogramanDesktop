from PyQt6 import QtWidgets, QtCore
from controllers.makanan_controller import load_makanan
from controllers.transaksi_controller import insert_transaksi
from models.database import get_connection
import sqlite3

def load_pembeli():
    """Load pembeli dari database pemesanan_makanan.db"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Coba query dengan kolom 'nama', jika gagal coba 'nama_pembeli'
        try:
            cursor.execute("SELECT id_pembeli, nama FROM pembeli")
        except sqlite3.OperationalError:
            cursor.execute("SELECT id_pembeli, nama_pembeli as nama FROM pembeli")
        
        rows = cursor.fetchall()
        result = []
        for r in rows:
            if isinstance(r, sqlite3.Row):
                result.append(dict(r))
            else:
                result.append({"id_pembeli": r[0], "nama": r[1]})
        return result
    except Exception as e:
        print(f"Error load pembeli: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def load_kasir():
    """Load kasir dari database pemesanan_makanan.db"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Coba query dengan kolom 'nama', jika gagal coba 'nama_kasir'
        try:
            cursor.execute("SELECT id_kasir, nama FROM kasir")
        except sqlite3.OperationalError:
            cursor.execute("SELECT id_kasir, nama_kasir as nama FROM kasir")
        
        rows = cursor.fetchall()
        result = []
        for r in rows:
            if isinstance(r, sqlite3.Row):
                result.append(dict(r))
            else:
                result.append({"id_kasir": r[0], "nama": r[1]})
        return result
    except Exception as e:
        print(f"Error load kasir: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

class TransaksiView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaksi Pembelian")
        self.resize(900, 600)
        
        self.detail_items = []  # Simpan detail transaksi sementara

        mainLayout = QtWidgets.QVBoxLayout(self)

        # ===== SECTION HEADER: Pembeli / Kasir (dari DB) =====
        headerFrame = QtWidgets.QFrame()
        headerLayout = QtWidgets.QHBoxLayout(headerFrame)

        # Pembeli (dari DB, hanya dropdown, tidak editable)
        headerLayout.addWidget(QtWidgets.QLabel("Pembeli:"))
        self.comboPembeli = QtWidgets.QComboBox()
        self.data_pembeli = load_pembeli()
        for p in self.data_pembeli:
            self.comboPembeli.addItem(p.get("nama", "Pembeli"), p.get("id_pembeli"))
        
        if len(self.data_pembeli) == 0:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tidak ada data pembeli di database!")
        
        headerLayout.addWidget(self.comboPembeli)
        headerLayout.addSpacing(40)

        # Kasir (dari DB, hanya dropdown, tidak editable)
        headerLayout.addWidget(QtWidgets.QLabel("Kasir:"))
        self.comboKasir = QtWidgets.QComboBox()
        self.data_kasir = load_kasir()
        for k in self.data_kasir:
            self.comboKasir.addItem(k.get("nama", "Kasir"), k.get("id_kasir"))
        
        if len(self.data_kasir) == 0:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tidak ada data kasir di database!")
        
        headerLayout.addWidget(self.comboKasir)
        headerLayout.addStretch()

        mainLayout.addWidget(headerFrame)

        # ===== SECTION INPUT ITEM =====
        inputFrame = QtWidgets.QGroupBox("Tambah Item Makanan")
        inputLayout = QtWidgets.QFormLayout(inputFrame)

        # Dropdown Pilih Makanan
        self.comboMakanan = QtWidgets.QComboBox()
        raw_makanan = load_makanan()
        self.data_makanan = [dict(r) if isinstance(r, sqlite3.Row) else r for r in raw_makanan]
        for m in self.data_makanan:
            self.comboMakanan.addItem(m.get("nama_makanan", "Unknown"), m.get("id_makanan"))

        # Harga otomatis
        self.txtHarga = QtWidgets.QLineEdit()
        self.txtHarga.setReadOnly(True)

        # Input Qty
        self.txtQty = QtWidgets.QSpinBox()
        self.txtQty.setRange(1, 100)
        self.txtQty.setValue(1)

        # Diskon per item (persen)
        self.spinDiskonItem = QtWidgets.QSpinBox()
        self.spinDiskonItem.setRange(0, 100)
        self.spinDiskonItem.setValue(0)
        self.spinDiskonItem.setSuffix(" %")

        # Subtotal otomatis (setelah diskon)
        self.txtSubtotal = QtWidgets.QLineEdit()
        self.txtSubtotal.setReadOnly(True)

        # Tombol Tambah Item
        self.btnTambahItem = QtWidgets.QPushButton("+ Tambah Item")
        self.btnTambahItem.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")

        inputLayout.addRow("Nama Makanan:", self.comboMakanan)
        inputLayout.addRow("Harga:", self.txtHarga)
        inputLayout.addRow("Qty:", self.txtQty)
        inputLayout.addRow("Diskon (item):", self.spinDiskonItem)
        inputLayout.addRow("Subtotal (setelah diskon):", self.txtSubtotal)
        inputLayout.addRow("", self.btnTambahItem)

        mainLayout.addWidget(inputFrame)

        # ===== SECTION TABEL DETAIL =====
        detailFrame = QtWidgets.QGroupBox("Detail Transaksi")
        detailLayout = QtWidgets.QVBoxLayout(detailFrame)

        # Tabel detail transaksi
        self.tabelDetail = QtWidgets.QTableWidget()
        self.tabelDetail.setColumnCount(6)
        self.tabelDetail.setHorizontalHeaderLabels(["Makanan", "Qty", "Harga", "Diskon (%)", "Subtotal", "Hapus"])
        self.tabelDetail.setColumnWidth(0, 300)
        self.tabelDetail.setColumnWidth(1, 60)
        self.tabelDetail.setColumnWidth(2, 120)
        self.tabelDetail.setColumnWidth(3, 100)
        self.tabelDetail.setColumnWidth(4, 140)
        self.tabelDetail.setColumnWidth(5, 80)

        detailLayout.addWidget(self.tabelDetail)
        mainLayout.addWidget(detailFrame)

        # ===== SECTION TOTAL =====
        totalFrame = QtWidgets.QHBoxLayout()
        totalFrame.addStretch()
        
        lblTotal = QtWidgets.QLabel("Total Harga:")
        lblTotal.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.txtTotal = QtWidgets.QLineEdit()
        self.txtTotal.setReadOnly(True)
        self.txtTotal.setText("Rp 0")
        self.txtTotal.setStyleSheet("font-weight: bold; font-size: 14px; background-color: #fff3cd;")
        self.txtTotal.setMaximumWidth(180)

        totalFrame.addWidget(lblTotal)
        totalFrame.addWidget(self.txtTotal)
        mainLayout.addLayout(totalFrame)

        # ===== SECTION BUTTON =====
        btnLayout = QtWidgets.QHBoxLayout()
        self.btnSimpan = QtWidgets.QPushButton("💾 Simpan Transaksi")
        self.btnSimpan.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.btnBatal = QtWidgets.QPushButton("❌ Batal")
        self.btnBatal.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")

        btnLayout.addStretch()
        btnLayout.addWidget(self.btnSimpan)
        btnLayout.addWidget(self.btnBatal)
        mainLayout.addLayout(btnLayout)

        # ===== EVENT =====
        self.comboMakanan.currentIndexChanged.connect(self.updateHargaSubtotal)
        self.txtQty.valueChanged.connect(self.updateHargaSubtotal)
        self.spinDiskonItem.valueChanged.connect(self.updateHargaSubtotal)
        self.btnTambahItem.clicked.connect(self.tambahItem)
        self.btnSimpan.clicked.connect(self.simpanTransaksi)
        self.btnBatal.clicked.connect(self.reject)

        self.updateHargaSubtotal()
        self.updateTotal()

    def updateHargaSubtotal(self):
        """Update harga dan subtotal saat makanan, qty, atau diskon item berubah"""
        if len(self.data_makanan) == 0:
            return
        idx = self.comboMakanan.currentIndex()
        harga = int(self.data_makanan[idx].get("harga_default", 0))
        qty = int(self.txtQty.value())
        diskon_pct = int(self.spinDiskonItem.value())
        subtotal_raw = harga * qty
        diskon_amt = (subtotal_raw * diskon_pct) // 100
        subtotal = subtotal_raw - diskon_amt

        self.txtHarga.setText(f"Rp {harga:,}")
        self.txtSubtotal.setText(f"Rp {subtotal:,}")

    def tambahItem(self):
        """Tambah item ke tabel detail (dengan diskon per item)"""
        if len(self.data_makanan) == 0:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tidak ada makanan di database!")
            return
        
        idx = self.comboMakanan.currentIndex()
        id_makanan = self.comboMakanan.itemData(idx)
        nama_makanan = self.comboMakanan.currentText()
        harga = int(self.data_makanan[idx].get("harga_default", 0))
        qty = int(self.txtQty.value())
        diskon_pct = int(self.spinDiskonItem.value())
        subtotal_raw = harga * qty
        diskon_amt = (subtotal_raw * diskon_pct) // 100
        subtotal = subtotal_raw - diskon_amt

        # unique item id
        item_id = (self.detail_items[-1]["item_id"] + 1) if self.detail_items else 1
        self.detail_items.append({
            "item_id": item_id,
            "id_makanan": id_makanan,
            "nama_makanan": nama_makanan,
            "harga_satuan": harga,
            "kuantitas": qty,
            "diskon_pct": diskon_pct,
            "subtotal": subtotal
        })

        # Tambah row ke tabel
        row = self.tabelDetail.rowCount()
        self.tabelDetail.insertRow(row)
        self.tabelDetail.setItem(row, 0, QtWidgets.QTableWidgetItem(nama_makanan))
        self.tabelDetail.setItem(row, 1, QtWidgets.QTableWidgetItem(str(qty)))
        self.tabelDetail.setItem(row, 2, QtWidgets.QTableWidgetItem(f"Rp {harga:,}"))
        self.tabelDetail.setItem(row, 3, QtWidgets.QTableWidgetItem(str(diskon_pct)))
        self.tabelDetail.setItem(row, 4, QtWidgets.QTableWidgetItem(f"Rp {subtotal:,}"))

        # Tombol hapus
        btnHapus = QtWidgets.QPushButton("Hapus")
        btnHapus.setStyleSheet("background-color: #f44336; color: white;")
        btnHapus.clicked.connect(lambda checked, iid=item_id: self.hapusItem(iid))
        self.tabelDetail.setCellWidget(row, 5, btnHapus)

        # Reset form input
        self.txtQty.setValue(1)
        self.spinDiskonItem.setValue(0)
        self.updateHargaSubtotal()
        self.updateTotal()

    def hapusItem(self, item_id):
        """Hapus item dari list berdasarkan item_id"""
        self.detail_items = [item for item in self.detail_items if item["item_id"] != item_id]
        self.refreshTable()
        self.updateTotal()

    def refreshTable(self):
        """Refresh tampilan tabel dari detail_items"""
        self.tabelDetail.setRowCount(0)
        for item in self.detail_items:
            row = self.tabelDetail.rowCount()
            self.tabelDetail.insertRow(row)
            self.tabelDetail.setItem(row, 0, QtWidgets.QTableWidgetItem(item["nama_makanan"]))
            self.tabelDetail.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item["kuantitas"])))
            self.tabelDetail.setItem(row, 2, QtWidgets.QTableWidgetItem(f"Rp {item['harga_satuan']:,}"))
            self.tabelDetail.setItem(row, 3, QtWidgets.QTableWidgetItem(str(item.get("diskon_pct", 0))))
            self.tabelDetail.setItem(row, 4, QtWidgets.QTableWidgetItem(f"Rp {item['subtotal']:,}"))
            btnHapus = QtWidgets.QPushButton("Hapus")
            btnHapus.setStyleSheet("background-color: #f44336; color: white;")
            btnHapus.clicked.connect(lambda checked, iid=item["item_id"]: self.hapusItem(iid))
            self.tabelDetail.setCellWidget(row, 5, btnHapus)

    def updateTotal(self):
        """Hitung total dari semua item"""
        total = sum([item["subtotal"] for item in self.detail_items])
        self.txtTotal.setText(f"Rp {total:,}")

    def simpanTransaksi(self):
        """Simpan transaksi dan detail ke database"""
        if len(self.detail_items) == 0:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tambahkan minimal 1 item makanan!")
            return

        try:
            total = sum([item["subtotal"] for item in self.detail_items])
            id_pembeli = self.comboPembeli.currentData()
            id_kasir = self.comboKasir.currentData()
            id_voucher = None

            insert_transaksi(self.detail_items, total, id_pembeli=id_pembeli, id_kasir=id_kasir, id_voucher=id_voucher)
            
            QtWidgets.QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan!")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menyimpan: {str(e)}")