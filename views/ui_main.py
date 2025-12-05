from PyQt6 import QtWidgets, QtCore, QtGui
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

        # ====== HEADER ======
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

        hLayout.addWidget(labelTitle)
        hLayout.addWidget(labelTagline)
        mainLayout.addWidget(header)

        # ===== FILTER SECTION =====
        filterFrame = QtWidgets.QFrame()
        filterLayout = QtWidgets.QHBoxLayout(filterFrame)

        self.comboKategori = QtWidgets.QComboBox()
        self.comboKategori.addItem("Semua Kategori")

        self.sliderHarga = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.sliderHarga.setRange(0, 50000)
        self.sliderHarga.setValue(50000)
        self.sliderHargaLabel = QtWidgets.QLabel("Max Harga: 50000")

        filterLayout.addWidget(QtWidgets.QLabel("Kategori:"))
        filterLayout.addWidget(self.comboKategori)
        filterLayout.addSpacing(30)
        filterLayout.addWidget(QtWidgets.QLabel("Harga Maks:"))
        filterLayout.addWidget(self.sliderHarga)
        filterLayout.addWidget(self.sliderHargaLabel)

        mainLayout.addWidget(filterFrame)

        # ===== CARD GRID =====
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)

        self.container = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(self.container)
        self.grid.setSpacing(15)

        self.data = load_makanan()

        # Isi kategori pada filter dropdown
        kategori_set = sorted(list(set([
            m["kategori"] if "kategori" in m.keys() else m["jenis_makanan"]
            for m in self.data
        ])))
        for j in kategori_set:
            self.comboKategori.addItem(j)

        self.filtered_data = self.data.copy()
        self.fillCards()

        # Event Filter
        self.comboKategori.currentTextChanged.connect(self.applyFilter)
        self.sliderHarga.valueChanged.connect(self.applyFilter)

        self.scrollArea.setWidget(self.container)
        mainLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

    # ===== UPDATE CARDS =====
    def fillCards(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget)
            widget.deleteLater()

        r = c = 0
        for m in self.filtered_data:
            card = CardWidget(m["nama_makanan"], m["harga_default"], m["nama_gambar"])
            self.grid.addWidget(card, r, c)
            c += 1
            if c == 3:
                c = 0
                r += 1

    # ===== FILTER ACTION =====
    def applyFilter(self):
        selectedKategori = self.comboKategori.currentText()
        maxHarga = self.sliderHarga.value()
        self.sliderHargaLabel.setText(f"Max Harga: {maxHarga}")

        self.filtered_data = []
        for m in self.data:
            kategori_value = m["kategori"] if "kategori" in m.keys() else m["jenis_makanan"]

            if (selectedKategori == "Semua Kategori" or kategori_value == selectedKategori) and \
               int(m["harga_default"]) <= maxHarga:
                self.filtered_data.append(m)

        self.fillCards()