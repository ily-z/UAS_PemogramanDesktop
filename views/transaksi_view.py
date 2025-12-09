from PyQt6 import QtWidgets, QtCore
from controllers.makanan_controller import load_makanan
from controllers.transaksi_controller import insert_transaksi

class TransaksiView(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaksi Pembelian")
        self.resize(400, 250)

        layout = QtWidgets.QFormLayout(self)

        # Dropdown Pilih Makanan
        self.comboMakanan = QtWidgets.QComboBox()
        self.data_makanan = load_makanan()
        for m in self.data_makanan:
            self.comboMakanan.addItem(m["nama_makanan"])

        # Harga otomatis
        self.txtHarga = QtWidgets.QLineEdit()
        self.txtHarga.setReadOnly(True)

        # Input Qty
        self.txtQty = QtWidgets.QSpinBox()
        self.txtQty.setRange(1, 100)

        # Total otomatis
        self.txtTotal = QtWidgets.QLineEdit()
        self.txtTotal.setReadOnly(True)

        layout.addRow("Nama Makanan:", self.comboMakanan)
        layout.addRow("Harga:", self.txtHarga)
        layout.addRow("Qty:", self.txtQty)
        layout.addRow("Total:", self.txtTotal)

        # Button Simpan
        self.btnSimpan = QtWidgets.QPushButton("Simpan Transaksi")
        layout.addRow(self.btnSimpan)

        # Event
        self.comboMakanan.currentIndexChanged.connect(self.updateHargaTotal)
        self.txtQty.valueChanged.connect(self.updateHargaTotal)
        self.btnSimpan.clicked.connect(self.simpanTransaksi)

        self.updateHargaTotal()

    def updateHargaTotal(self):
        idx = self.comboMakanan.currentIndex()
        harga = int(self.data_makanan[idx]["harga_default"])
        qty = int(self.txtQty.value())
        total = harga * qty
        self.txtHarga.setText(str(harga))
        self.txtTotal.setText(str(total))

    def simpanTransaksi(self):
        idx = self.comboMakanan.currentIndex()
        id_makanan = self.data_makanan[idx]["id_makanan"]
        qty = int(self.txtQty.value())
        total = int(self.txtTotal.text())

        insert_transaksi(id_makanan, qty, total)
        
        QtWidgets.QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan!")
        self.accept()