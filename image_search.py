from PIL import Image
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,
                               QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (Slot, Qt)


class NewWindow(QWidget):
    def __init__(self, str):
        super().__init__()
        self.text = QLabel(str)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.search_label = QLabel('Hello, world!')
        hbox = QHBoxLayout()
        hbox.addWidget(self.search_label)
        self.setLayout(hbox)
        self.setWindowTitle("Image Search")


app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
