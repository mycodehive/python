"""
Description :  Notepad application with tree structure using PySide6
Location : https://github.com/sahuni/python
Date : 2025.01.12
"""
import sys
import os
import json
from PySide6.QtWidgets import (
    QFontDialog,
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QSplitter, QFileDialog, QMessageBox, QMenu, QVBoxLayout, QWidget, QInputDialog, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QAction, QKeySequence, QFont
from PySide6.QtCore import Qt

TREE_FILE = ""
NOTES_DIR = ""

class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad with Tree Structure")
        self.resize(800, 600)
        self.init_ui()
        self.load_tree()

    def select_save_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory to Save Notes")
        if folder:
            global TREE_FILE, NOTES_DIR
            NOTES_DIR = os.path.join(folder, "notes")
            TREE_FILE = os.path.join(folder, "tree_structure.json")
            if not os.path.exists(NOTES_DIR):
                os.makedirs(NOTES_DIR)
        else:
            QMessageBox.warning(self, "Warning", "No folder selected. The application will now close.")
            sys.exit()

    

    def init_ui(self):
        self.editor_font_size = 12  # 기본 폰트 크기 설정
        self.select_save_directory()
        splitter = QSplitter(Qt.Horizontal)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.load_note)
        self.tree.itemDoubleClicked.connect(self.load_note)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_tree_menu)
        splitter.addWidget(self.tree)

        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.auto_save_note)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(1, 1)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

        self.create_menu()
        self.create_shortcuts()
        self.create_window_buttons()

        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

    def create_menu(self):
        font_action = QAction("Change Font", self)
        font_action.triggered.connect(self.change_font)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_note)
        save_all_action = QAction("Save All", self)
        save_all_action.triggered.connect(self.save_all_notes)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(save_action)
        file_menu.addAction(save_all_action)
        file_menu.addAction(font_action)

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.editor_font_size += 1
            else:
                self.editor_font_size -= 1
                if self.editor_font_size < 1:
                    self.editor_font_size = 1
            font = self.editor.font()
            font.setPointSize(self.editor_font_size)
            self.editor.setFont(font)
            event.accept()
        else:
            super().wheelEvent(event)

    def create_shortcuts(self):
        save_shortcut = QAction("Save", self)
        save_shortcut.setShortcut(QKeySequence.Save)
        save_shortcut.triggered.connect(self.save_note)
        self.addAction(save_shortcut)

        save_all_shortcut = QAction("Save All", self)
        save_all_shortcut.setShortcut("Ctrl+Shift+S")
        save_all_shortcut.triggered.connect(self.save_all_notes)
        self.addAction(save_all_shortcut)

    def create_window_buttons(self):
        minimize_button = QPushButton("_", self)
        minimize_button.clicked.connect(self.showMinimized)

        maximize_button = QPushButton("▢", self)
        maximize_button.clicked.connect(self.toggle_maximize)

        close_button = QPushButton("X", self)
        close_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(minimize_button)
        button_layout.addWidget(maximize_button)
        button_layout.addWidget(close_button)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        self.menuBar().setCornerWidget(button_widget, Qt.TopRightCorner)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def open_tree_menu(self, position):
        menu = QMenu()
        add_note_action = QAction("Add Note", self)
        add_note_action.triggered.connect(self.add_note)
        add_child_note_action = QAction("Add Child Note", self)
        add_child_note_action.triggered.connect(self.add_child_note)
        add_date_note_action = QAction("Add Today's Child Note", self)
        add_date_note_action.triggered.connect(self.add_today_child_note)
        rename_note_action = QAction("Rename Note", self)
        rename_note_action.triggered.connect(self.rename_note)
        delete_note_action = QAction("Delete Note", self)
        delete_note_action.triggered.connect(self.delete_note)
        menu.addAction(add_note_action)
        menu.addAction(add_child_note_action)
        menu.addAction(add_date_note_action)
        menu.addAction(rename_note_action)
        menu.addAction(delete_note_action)
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def delete_note(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            reply = QMessageBox.question(self, "Delete Note", f"Are you sure you want to delete '{selected_item.text(0)}'?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                note_path = selected_item.data(0, Qt.UserRole)
                if note_path and os.path.exists(note_path):
                    os.remove(note_path)
                parent = selected_item.parent()
                if parent:
                    parent.removeChild(selected_item)
                else:
                    index = self.tree.indexOfTopLevelItem(selected_item)
                    self.tree.takeTopLevelItem(index)
                self.save_tree()

    def rename_note(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            old_name = selected_item.text(0)
            new_name, ok = QInputDialog.getText(self, "Rename Note", "New name:", text=old_name)
            if ok and new_name:
                new_path = os.path.join(NOTES_DIR, f"{new_name}.txt")
                if os.path.exists(new_path):
                    QMessageBox.warning(self, "Warning", "A note with this name already exists.")
                    return
                old_path = selected_item.data(0, Qt.UserRole)
                if old_path and isinstance(old_path, str) and os.path.exists(old_path):
                    os.rename(old_path, new_path)
                selected_item.setText(0, new_name)
                selected_item.setData(0, Qt.UserRole, new_path)
                self.save_tree()

    def add_child_note(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            text, ok = QInputDialog.getText(self, "Add Child Note", "Child note name:")
            if ok and text:
                note_path = os.path.join(NOTES_DIR, f"{text}.txt")
                if not os.path.exists(note_path):
                    with open(note_path, "w", encoding="utf-8") as file:
                        file.write("")
                child_item = QTreeWidgetItem([text])
                child_item.setData(0, Qt.UserRole, note_path)
                selected_item.addChild(child_item)
                selected_item.setExpanded(True)
                self.save_tree()

    def add_note(self):
        text, ok = QInputDialog.getText(self, "Add Note", "Note name:")
        if ok and text:
            note_path = os.path.join(NOTES_DIR, f"{text}.txt")
            if not os.path.exists(note_path):
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write("")
            item = QTreeWidgetItem([text])
            item.setData(0, Qt.UserRole, note_path)
            self.tree.addTopLevelItem(item)
            self.save_tree()

    def add_today_child_note(self):
        from datetime import datetime
        selected_item = self.tree.currentItem()
        if selected_item:
            date_str = datetime.now().strftime("%Y-%m-%d")
            note_path = os.path.join(NOTES_DIR, f"{date_str}.txt")
            if not os.path.exists(note_path):
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write("")
            child_item = QTreeWidgetItem([date_str])
            child_item.setData(0, Qt.UserRole, note_path)
            selected_item.addChild(child_item)
            selected_item.setExpanded(True)
            self.save_tree()

    def load_note(self, item):
        note_path = item.data(0, Qt.UserRole)
        if note_path and os.path.exists(note_path):
            with open(note_path, "r", encoding="utf-8") as file:
                self.editor.setPlainText(file.read())
        else:
            self.editor.clear()

    def auto_save_note(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            note_path = selected_item.data(0, Qt.UserRole)
            if note_path:
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(self.editor.toPlainText())

    def save_note(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            note_path = selected_item.data(0, Qt.UserRole)
            if note_path:
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(self.editor.toPlainText())
                QMessageBox.information(self, "Saved", f"Note saved to {note_path}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a note to save.")

    def load_tree(self):
        if os.path.exists(TREE_FILE):
            try:
                with open(TREE_FILE, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        tree_data = json.loads(content)
                    else:
                        tree_data = []
            except (json.JSONDecodeError, FileNotFoundError):
                QMessageBox.warning(self, "Error", "Tree structure file is corrupted or empty.")
                tree_data = []

            def load_item(data):
                item = QTreeWidgetItem([data["name"]])
                note_path = data.get("path")
                if note_path and not os.path.exists(note_path):
                    with open(note_path, "w", encoding="utf-8") as file:
                        file.write("")
                item.setData(0, Qt.UserRole, note_path)
                for child in data.get("children", []):
                    item.addChild(load_item(child))
                return item

            for data in tree_data:
                self.tree.addTopLevelItem(load_item(data))

    def save_tree(self):
        def serialize_item(item):
            return {
                "name": item.text(0),
                "path": item.data(0, Qt.UserRole),
                "children": [serialize_item(item.child(i)) for i in range(item.childCount())]
            }
        tree_data = [serialize_item(self.tree.topLevelItem(i)) for i in range(self.tree.topLevelItemCount())]
        with open(TREE_FILE, "w", encoding="utf-8") as file:
            json.dump(tree_data, file, indent=4)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok and isinstance(font, QFont):
            self.editor.setCurrentFont(font)  # 에디터에 즉시 적용
            self.tree.setFont(font)

    def save_all_notes(self):
        def save_item(item):
            note_path = item.data(0, Qt.UserRole)
            if note_path:
                content = ""
                if self.tree.currentItem() == item:
                    content = self.editor.toPlainText()
                elif os.path.exists(note_path):
                    with open(note_path, "r", encoding="utf-8") as file:
                        content = file.read()
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(content)
            for i in range(item.childCount()):
                save_item(item.child(i))
        for i in range(self.tree.topLevelItemCount()):
            save_item(self.tree.topLevelItem(i))
        QMessageBox.information(self, "Saved", "All notes have been saved.")
        def save_item(item):
            note_path = item.data(0, Qt.UserRole)
            if note_path and os.path.exists(note_path):
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(self.editor.toPlainText())
            for i in range(item.childCount()):
                save_item(item.child(i))
        for i in range(self.tree.topLevelItemCount()):
            save_item(self.tree.topLevelItem(i))
        QMessageBox.information(self, "Saved", "All notes have been saved.")
        selected_item = self.tree.currentItem()
        if selected_item:
            note_path = selected_item.data(0, Qt.UserRole)
            if note_path:
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(self.editor.toPlainText())
                QMessageBox.information(self, "Saved", f"Note saved to {note_path}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a note to save.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotepadApp()
    window.show()
    sys.exit(app.exec())
