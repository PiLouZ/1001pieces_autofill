import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QHBoxLayout, QLabel, QHeaderView
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

DB_PATH = "appareils.db"

class TableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compléter les champs vides")
        self.resize(1000, 600)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Copiez-collez vos données dans le tableau (Ctrl+V / Cmd+V)"))

        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Type", "Manufacturer", "Reference Modèle", "Commercial Reference", "Other Reference", "Treatment Column"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)

        btn_layout = QHBoxLayout()
        self.complete_btn = QPushButton("Compléter les champs vides")
        self.complete_btn.clicked.connect(self.completer_champs_vides)
        btn_layout.addWidget(self.complete_btn)

        self.save_btn = QPushButton("Mémoriser les données")
        self.save_btn.clicked.connect(self.enregistrer_dans_bdd)
        btn_layout.addWidget(self.save_btn)

        self.export_btn = QPushButton("Exporter en CSV")
        self.export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.export_btn)

        self.layout.addLayout(btn_layout)
        self.table.setFocus()

        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS appareils (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    col_a TEXT,
                    col_b TEXT,
                    col_c TEXT,
                    col_d TEXT,
                    col_e TEXT,
                    col_f TEXT,
                    UNIQUE(col_a, col_b, col_c, col_d)
                )
            ''')
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_col_c ON appareils(col_c)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_col_d ON appareils(col_d)")

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            self.handle_paste()
        elif event.matches(QKeySequence("Ctrl+Up")):
            self.duplicate_cell(-1)
        elif event.matches(QKeySequence("Ctrl+Down")):
            self.duplicate_cell(1)
        else:
            super().keyPressEvent(event)

    def handle_paste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        rows = text.strip().split('\n')
        data = [row.split('\t') for row in rows]

        self.table.setRowCount(len(data))
        self.table.setColumnCount(max(len(r) for r in data))

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(val))

    def duplicate_cell(self, direction):
        row = self.table.currentRow()
        col = self.table.currentColumn()
        if row < 0 or col < 0:
            return
        item = self.table.item(row, col)
        if item:
            text = item.text()
            new_row = row + direction
            if 0 <= new_row < self.table.rowCount():
                self.table.setItem(new_row, col, QTableWidgetItem(text))

    def completer_champs_vides(self):
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        data = [[self.table.item(i, j).text() if self.table.item(i, j) else "" for j in range(col_count)] for i in range(row_count)]

        def is_empty(cell):
            return cell.strip() == ""

        remaining = 0
        for i, row in enumerate(data):
            if is_empty(row[0]) or is_empty(row[1]):
                completed = False
                col_c, col_d = row[2], row[3] if len(row) > 3 else ""

                cur = self.conn.cursor()

                cur.execute("""
                    SELECT col_a, col_b FROM appareils 
                    WHERE col_c = ? AND col_a IS NOT NULL AND col_b IS NOT NULL
                    LIMIT 1
                """, (col_c,))
                match = cur.fetchone()
                if match:
                    row[0], row[1] = match
                    completed = True

                if not completed:
                    cur.execute("""
                        SELECT col_a, col_b FROM appareils 
                        WHERE col_d = ? AND col_a IS NOT NULL AND col_b IS NOT NULL
                        LIMIT 1
                    """, (col_d,))
                    match = cur.fetchone()
                    if match:
                        row[0], row[1] = match
                        completed = True

                if not completed:
                    remaining += 1

        if remaining > 0:
            QMessageBox.information(self, "Complétion", f"Complétion terminée. {remaining} lignes incomplètes restantes.")
        else:
            QMessageBox.information(self, "Complétion", "Toutes les lignes ont été complétées avec succès.")

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(val))

    def enregistrer_dans_bdd(self):
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        new_rows = 0

        with self.conn:
            for i in range(row_count):
                row = [self.table.item(i, j).text() if self.table.item(i, j) else "" for j in range(col_count)]
                if len(row) < 6:
                    row += [""] * (6 - len(row))
                try:
                    self.conn.execute("""
                        INSERT OR IGNORE INTO appareils (col_a, col_b, col_c, col_d, col_e, col_f)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, tuple(row[:6]))
                    new_rows += 1
                except Exception as e:
                    print("Erreur d'insertion:", e)

        QMessageBox.information(self, "Enregistrement terminé", f"{new_rows} lignes ajoutées à la base.")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Fichiers CSV (*.csv)")
        if path:
            with open(path, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in range(self.table.rowCount()):
                    rowdata = [self.table.item(row, col).text() if self.table.item(row, col) else "" for col in range(self.table.columnCount())]
                    writer.writerow(rowdata)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TableApp()
    win.show()
    sys.exit(app.exec_())
