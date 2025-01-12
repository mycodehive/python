"""
Description :  This script is a simple SQLite CRUD application using PySide6.
Location : https://github.com/sahuni/python
Date : 2025.01.12
"""
import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox
)

TABLE_SCHEMA = "items"

class SQLiteCRUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite CRUD App")
        self.resize(600, 400)
        self.db_path = ""
        self.conn = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.file_select_button = QPushButton("SQLite 파일 선택")
        self.file_select_button.clicked.connect(self.select_db_file)
        self.layout.addWidget(self.file_select_button)

        self.create_db_button = QPushButton("SQLite 파일 만들기")
        self.create_db_button.clicked.connect(self.create_db_file)
        self.layout.addWidget(self.create_db_button)

        self.selected_file_label = QLabel("선택된 파일: 없음")
        self.layout.addWidget(self.selected_file_label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.input_layout = QHBoxLayout()
        self.new_data_input = QLineEdit()
        self.new_data_input.setPlaceholderText("새 데이터 입력")
        self.input_layout.addWidget(self.new_data_input)

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_data)
        self.input_layout.addWidget(self.add_button)

        self.update_button = QPushButton("수정")
        self.update_button.clicked.connect(self.update_data)
        self.input_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_data)
        self.input_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.input_layout)

    def select_db_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SQLite 파일 선택", "", "SQLite Files (*.db *.sqlite)")
        if file_path:
            self.db_path = file_path
            self.selected_file_label.setText(f"선택된 파일: {file_path}")
            self.connect_to_db()

    def create_db_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "SQLite 파일 만들기", "", "SQLite Files (*.db *.sqlite)")
        if file_path:
            self.db_path = file_path
            self.selected_file_label.setText(f"생성된 파일: {file_path}")
            self.connect_to_db()

    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_table()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "DB 연결 오류", str(e))

    def create_table(self):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_SCHEMA} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
            self.conn.commit()

    def load_data(self):
        if not self.conn:
            return
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {TABLE_SCHEMA}")
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["ID", "이름"])
            for row_idx, row_data in enumerate(rows):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터 로딩 오류", str(e))

    def add_data(self):
        if not self.conn:
            QMessageBox.warning(self, "DB 오류", "데이터베이스 파일을 먼저 선택하세요.")
            return
        new_data = self.new_data_input.text()
        if not new_data:
            QMessageBox.warning(self, "입력 오류", "데이터를 입력하세요.")
            return
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"INSERT INTO {TABLE_SCHEMA} (name) VALUES (?)", (new_data,))
            self.conn.commit()
            self.new_data_input.clear()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터 추가 오류", str(e))

    def update_data(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "선택 오류", "수정할 항목을 선택하세요.")
            return
        row = selected_items[0].row()
        item_id = self.table.item(row, 0).text()
        new_name = self.new_data_input.text()
        if not new_name:
            QMessageBox.warning(self, "입력 오류", "새 이름을 입력하세요.")
            return
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"UPDATE {TABLE_SCHEMA} SET name = ? WHERE id = ?", (new_name, item_id))
            self.conn.commit()
            self.new_data_input.clear()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터 수정 오류", str(e))

    def delete_data(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "선택 오류", "삭제할 항목을 선택하세요.")
            return
        row = selected_items[0].row()
        item_id = self.table.item(row, 0).text()
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {TABLE_SCHEMA} WHERE id = ?", (item_id,))
            self.conn.commit()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터 삭제 오류", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SQLiteCRUDApp()
    window.show()
    sys.exit(app.exec())
