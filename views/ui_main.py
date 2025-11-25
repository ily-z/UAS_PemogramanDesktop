from PyQt6 import QtWidgets, QtCore
from controllers.makanan_controller import load_makanan
from views.components.card_widget import CardWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Menu Makanan")
        MainWindow.resize(950, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # ===== HEADER =====
        header = QtWidgets.QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #d4b178, stop:0.4 #c89d5a, stop:1 #2a1d0f
            );
        """)
        hLayout = QtWidgets.QVBoxLayout(header)

        labelTitle = QtWidgets.QLabel("⭐ Golden Bites Resto ⭐")
        labelTitle.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        labelTagline = QtWidgets.QLabel("Premium Taste • Traditional Style")
        labelTagline.setStyleSheet("font-size: 14px; color: #fce9c5;")
        labelTagline.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        hLayout.addStretch()
        hLayout.addWidget(labelTitle)
        hLayout.addWidget(labelTagline)
        hLayout.addStretch()

        mainLayout.addWidget(header)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 920, 720))
        self.scrollArea.setWidgetResizable(True)

        self.container = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(self.container)
        self.grid.setSpacing(15)

        data = load_makanan()

        r = c = 0
        for m in data:
            nama = m["nama_makanan"]
            harga = m["harga_default"]
            gambar = m["nama_gambar"]
            card = CardWidget(nama, harga, gambar)
            self.grid.addWidget(card, r, c)
            c += 1
            if c == 3:
                c = 0
                r += 1

        self.scrollArea.setWidget(self.container)
        mainLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
