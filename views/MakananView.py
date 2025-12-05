# views/makanan_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QWidget as W, QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MakananView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelola Makanan")
        self.resize(820, 540)

        main = QVBoxLayout(self)
        main.setContentsMargins(12, 12, 12, 12)
        main.setSpacing(10)

        # ====================== HEADER BAR ==========================
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #d4b178, stop:0.4 #c89d5a, stop:1 #2a1d0f
            );
            border-radius: 10px;
        """)
        
        hLay = QHBoxLayout(header)
        label_title = QLabel("🍽️ Kelola Data Makanan")
        label_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        hLay.addWidget(label_title)
        main.addWidget(header)

        # ====================== ADD BUTTON ==========================
        self.btn_add = QPushButton("➕ Tambah Makanan")
        self.btn_add.setFixedHeight(42)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #c89d5a;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #ad864f;
            }
        """)
        main.addWidget(self.btn_add)

        # ====================== TABLE ==========================
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nama", "Harga", "Aksi"])
        self.table.setColumnHidden(0, False)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border-radius: 8px;
                font-size: 14px;
            }
            QHeaderView::section {
                background: #e5c48f;
                color: black;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(self.table.styleSheet() + 
            "QTableWidget::item:alternate { background: #fbf3e1; }"
        )

        main.addWidget(self.table)

    def set_table_data(self, rows):
        """rows: list of tuples (id, name, price)"""
        self.table.setRowCount(0)

        for r_idx, row in enumerate(rows):
            self.table.insertRow(r_idx)

            # ID — hidden internally but visually OK
            id_item = QTableWidgetItem(str(row[0]))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r_idx, 0, id_item)

            # Nama
            name_item = QTableWidgetItem(row[1])
            self.table.setItem(r_idx, 1, name_item)

            # Harga
            price_item = QTableWidgetItem(f"Rp {row[2]:,}".replace(",", "."))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r_idx, 2, price_item)

            # Button area
            btn_edit = QPushButton("✏ Edit")
            btn_delete = QPushButton("🗑 Hapus")

            btn_edit.setStyleSheet("""
                QPushButton {
                    background: #0099cc;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 6px;
                }
                QPushButton:hover { background: #0077aa; }
            """)

            btn_delete.setStyleSheet("""
                QPushButton {
                    background: #cc4444;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 6px;
                }
                QPushButton:hover { background: #bb3333; }
            """)

            box = QHBoxLayout()
            cell = W()
            box.addWidget(btn_edit)
            box.addWidget(btn_delete)
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setSpacing(8)
            cell.setLayout(box)
            self.table.setCellWidget(r_idx, 3, cell)

            # expose signals
            btn_edit.clicked.connect(lambda checked, r=row: getattr(self, "on_edit", lambda x: None)(r))
            btn_delete.clicked.connect(lambda checked, r=row: getattr(self, "on_delete", lambda x: None)(r))

    def confirm_delete(self, parent=None):
        ret = QMessageBox.question(
            parent or self, "Konfirmasi Hapus",
            "Yakin ingin menghapus item ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return ret == QMessageBox.StandardButton.Yes

    def show_info(self, text):
        QMessageBox.information(self, "Info", text)
