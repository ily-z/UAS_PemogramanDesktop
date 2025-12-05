from models.database import get_connection
from models.makanan_model import MakananModel, get_all_makanan
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
# Asumsi: Anda memiliki MakananView di views/MakananView.py
from views.MakananView import MakananView


##### HELPER FUNCTIONS – dipakai langsung di UI #####

def load_makanan():
    """Memuat semua data makanan dari model/database."""
    return get_all_makanan()

def delete_makanan(id_makanan):
    """Menghapus data makanan berdasarkan ID."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM makanan WHERE id_makanan = ?", (id_makanan,))
    conn.commit()
    conn.close()

def insert_makanan(nama_makanan, harga_default, kategori, nama_gambar):
    """Menyimpan data makanan baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO makanan (nama_makanan, harga_default, kategori, nama_gambar)
        VALUES (?, ?, ?, ?)
    """, (nama_makanan, harga_default, kategori, nama_gambar))
    conn.commit()
    conn.close()

def update_makanan(id_makanan, nama_makanan, harga_default, kategori, nama_gambar):
    """Memperbarui data makanan di database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE makanan
        SET nama_makanan = ?, harga_default = ?, kategori = ?, nama_gambar = ?
        WHERE id_makanan = ?
    """, (nama_makanan, harga_default, kategori, nama_gambar, id_makanan))
    conn.commit()
    conn.close()


##### MakananForm (DIPERLUKAN UNTUK CONTROLLER/VIEW) #####

class MakananForm(QDialog):
    def __init__(self, parent=None, data=None):
        """
        data format:
        None → mode insert
        (id, nama, harga, kategori, gambar) → edit mode
        """
        super().__init__(parent)
        self.setWindowTitle("Form Makanan")
        self.resize(350, 220)

        self.data = data
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Nama Makanan:"))
        self.input_name = QLineEdit("" if data is None else data[1])
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Harga Default:"))
        self.input_price = QLineEdit("" if data is None else str(data[2]))
        layout.addWidget(self.input_price)

        layout.addWidget(QLabel("Kategori:"))
        self.input_category = QComboBox()
        self.input_category.addItems(["Makanan", "Minuman", "Snack", "Other"])
        if data:
            idx = self.input_category.findText(data[3])
            if idx >= 0:
                self.input_category.setCurrentIndex(idx)
        layout.addWidget(self.input_category)

        layout.addWidget(QLabel("Nama File Gambar:"))
        self.input_image = QLineEdit("" if data is None else data[4])
        layout.addWidget(self.input_image)

        btn_save = QPushButton("✔ Simpan")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

    def get_form_data(self):
        return (
            self.input_name.text().strip(),
            self.input_price.text().strip(),
            self.input_category.currentText(),
            self.input_image.text().strip()
        )


##### MakananController (TIDAK ADA PERUBAHAN) #####

class MakananController:
    def __init__(self, parent=None):
        self.model = MakananModel()
        self.view = MakananView()
        self.parent = parent

        # ACTION BIND
        self.view.btn_add.clicked.connect(self.on_add)
        self.view.on_edit = self.on_edit
        self.view.on_delete = self.on_delete

        self.reload()
        self.view.show()

    def reload(self):
        rows = self.model.get_all()
        # Expected format:
        # (id, nama, harga, kategori, gambar)
        self.view.set_table_data(rows)

    def on_add(self):
        dlg = MakananForm(parent=self.view)
        if dlg.exec():
            name, price, kategori, img = dlg.get_form_data()

            if not (name and price.isdigit()):
                self.view.show_info("Nama dan harga wajib diisi dan harga harus angka.")
                return

            self.model.insert(name, int(price), kategori, img)
            self.reload()

    def on_edit(self, row):
        dlg = MakananForm(parent=self.view, data=row)
        if dlg.exec():
            name, price, kategori, img = dlg.get_form_data()

            if not (name and price.isdigit()):
                self.view.show_info("Nama dan harga wajib diisi dan harga harus angka.")
                return

            self.model.update(row[0], name, int(price), kategori, img)
            self.reload()

    def on_delete(self, row):
        # Asumsi: method confirm_delete di View sudah sesuai
        if self.view.confirm_delete(self.view):
            self.model.delete(row[0])
            self.reload()

    def close(self):
        self.model.close()
        self.view.close()