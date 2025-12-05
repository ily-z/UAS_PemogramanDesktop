from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton

class MakananForm(QDialog):
    def __init__(self, name="", price=""):
        super().__init__()
        self.setWindowTitle("Input Menu")

        layout = QVBoxLayout()

        self.inputName = QLineEdit(name)
        self.inputPrice = QLineEdit(str(price))

        layout.addWidget(QLabel("Nama:"))
        layout.addWidget(self.inputName)

        layout.addWidget(QLabel("Harga:"))
        layout.addWidget(self.inputPrice)

        btnSave = QPushButton("Simpan")
        btnSave.clicked.connect(self.accept)

        layout.addWidget(btnSave)
        self.setLayout(layout)

    def getData(self):
        return self.inputName.text(), self.inputPrice.text()
