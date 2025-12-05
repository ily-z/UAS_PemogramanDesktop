from PyQt6 import QtWidgets, QtCore, QtGui
from controllers.makanan_controller import MakananController, load_makanan
from views.components.card_widget import CardWidget
from views.components.form_makanan import FormMakanan
from controllers.makanan_controller import MakananController


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.makanan_ctrl = None
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

        # ====== MENU NAVIGASI SAMPING ======
        self.menuFrame = QtWidgets.QFrame()
        self.menuFrame.setFixedHeight(60)
        self.menuFrame.setStyleSheet("""
            background-color: #FFFFFF;
            border-bottom: 1px solid #ccc;
        """)

        menuLayout = QtWidgets.QHBoxLayout(self.menuFrame)
        menuLayout.setContentsMargins(10, 5, 10, 5)
        menuLayout.setSpacing(15)

        self.btnDashboard = QtWidgets.QPushButton(self.menuFrame)
        self.btnTransaksi = QtWidgets.QPushButton(self.menuFrame)
        self.btnLaporan = QtWidgets.QPushButton(self.menuFrame)
        self.btnKelolaMakanan = QtWidgets.QPushButton(self.menuFrame)
        self.btnKelolaMakanan.setObjectName("btnKelolaMakanan")
        self.btnKelolaMakanan.setText("Kelola Makanan")
        self.btnKelolaMakanan.setMinimumHeight(35)
        #self.btnKelolaMakanan.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # self.btnDashboard = QtWidgets.QPushButton("Dashboard")
        # self.btnTransaksi = QtWidgets.QPushButton("Transaksi")
        # self.btnLaporan = QtWidgets.QPushButton("Laporan")
        # self.btnKelolaMakanan = QtWidgets.QPushButton("Kelola Makanan")

        mainLayout.addWidget(self.menuFrame)
        self.btnKelolaMakanan.clicked.connect(self.open_makanan_crud)
        menuLayout.addWidget(self.btnDashboard)


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
            card = CardWidget(m, self.editRecord, self.deleteRecord)
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
    # ===== EDIT RECORD =====
    def editRecord(self, data):
        self.form = FormMakanan()
        self.form.setModeEdit(
            data["id_makanan"],
            data["nama_makanan"],
            str(data["harga_default"]),
            data["kategori"],
            data["nama_gambar"]
        )

        if self.form.exec():
            # Refresh data setelah update
            self.data = load_makanan()
            self.applyFilter()


    def open_makanan_crud(self):
    # jika mau single instance, simpan di self
        if not hasattr(self, "makanan_ctrl") or self.makanan_ctrl is None:
            self.makanan_ctrl = MakananController(parent=self)
        else:
            self.makanan_ctrl.view.show()
    
    # ===== DELETE RECORD =====
    def deleteRecord(self, data):
        confirm = QtWidgets.QMessageBox.question(
            None,
            "Hapus Data",
            f"Yakin hapus '{data['nama_makanan']}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            from controllers.makanan_controller import delete_makanan
            delete_makanan(data['id_makanan'])
            
            # Refresh data di UI
            self.data = load_makanan()
            self.applyFilter()
