from PyQt6 import QtWidgets
from controllers.makanan_controller import insert_makanan, update_makanan

class FormMakanan(QtWidgets.QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Form Makanan")
        self.resize(350, 200)
        self.data = data
        self.mode = "add"

        layout = QtWidgets.QFormLayout(self)

        self.inNama = QtWidgets.QLineEdit()
        self.inHarga = QtWidgets.QLineEdit()
        self.inKategori = QtWidgets.QLineEdit()
        self.inGambar = QtWidgets.QLineEdit()

        layout.addRow("Nama:", self.inNama)
        layout.addRow("Harga:", self.inHarga)
        layout.addRow("Kategori:", self.inKategori)
        layout.addRow("Nama Gambar:", self.inGambar)

        btnSubmit = QtWidgets.QPushButton("Simpan")
        btnSubmit.clicked.connect(self.simpanData)
        layout.addRow(btnSubmit)

        if self.data:  # isi data untuk edit
            self.inNama.setText(self.data["nama_makanan"])
            self.inHarga.setText(str(self.data["harga_default"]))
            self.inKategori.setText(self.data["kategori"])
            self.inGambar.setText(self.data["nama_gambar"])

    def getData(self):
        return {
            "nama_makanan": self.inNama.text(),
            "harga_default": int(self.inHarga.text()),
            "kategori": self.inKategori.text(),
            "nama_gambar": self.inGambar.text(),
        }
        
    def setModeEdit(self, id_makanan, nama, harga, kategori, gambar):
        self.mode = "edit"  # <-- TAMBAHKAN BARIS INI
    
        self.data = {
            "id_makanan": id_makanan,
            "nama_makanan": nama,
            "harga_default": harga,
            "kategori": kategori,
            "nama_gambar": gambar
        }
        self.inNama.setText(nama)
        self.inHarga.setText(harga)
        self.inKategori.setText(kategori)
        self.inGambar.setText(gambar)

    
    def simpanData(self):
        new_data = self.getData()

        if self.mode == "edit":
            update_makanan(
                self.data["id_makanan"],
                new_data["nama_makanan"],
                new_data["harga_default"],
                new_data["kategori"],
                new_data["nama_gambar"]
            )
        else:
            insert_makanan(
                new_data["nama_makanan"],
                new_data["harga_default"],
                new_data["kategori"],
                new_data["nama_gambar"]
            )

        self.accept()  # Tutup form setelah simpan
