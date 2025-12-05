from PyQt6 import QtWidgets, QtGui, QtCore

class CardWidget(QtWidgets.QWidget):
    def __init__(self, data, editCallback, deleteCallback):
        super().__init__()
        self.data = data
        self.editCallback = editCallback
        self.deleteCallback = deleteCallback

        self.setFixedSize(240, 360)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(6)

        # Gambar
        img_path = f"images/{data['nama_gambar']}"
        img_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(img_path).scaled(
            240, 150,
            QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        img_label.setPixmap(pixmap)
        img_label.setFixedHeight(150)
        layout.addWidget(img_label)

        # Nama makanan
        name_lbl = QtWidgets.QLabel(data["nama_makanan"])
        name_lbl.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        layout.addWidget(name_lbl)

        # Harga
        price_lbl = QtWidgets.QLabel(f"Rp {data['harga_default']:,}")
        price_lbl.setStyleSheet("font-size: 15px; background:#222; color: gold; padding:6px; border-radius:6px;")
        layout.addWidget(price_lbl)

        bottom = QtWidgets.QHBoxLayout()
        qty = QtWidgets.QSpinBox()
        qty.setStyleSheet("color: white;")
        qty.setFixedWidth(50)

        add_cart = QtWidgets.QPushButton("🛒")
        beli = QtWidgets.QPushButton("⚡ Beli")
        add_cart.setStyleSheet("background:#c7a06a; color:black; font-weight:bold; padding:4px;")
        beli.setStyleSheet("background:#e6d1a3; color:black; font-weight:bold; padding:4px;")

        bottom.addWidget(qty)
        bottom.addWidget(add_cart)
        bottom.addWidget(beli)
        layout.addLayout(bottom)

        # ===== TOMBOL EDIT & HAPUS =====
        actions = QtWidgets.QHBoxLayout()
        

        layout.addLayout(actions)

        layout.addStretch()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("background:#1b1b1b; border-radius:10px;")
        self.setLayout(layout)