# -----------------------------------------
# Author: Leonardo Villalobos
# Date: 3/18/2021
# Instructor: Professor Avner Biblarz
# Course: CST-205
# Description: Prompts the user to enter a search
# and select a filter. Displays the appropriate
# image and filter, depending on the image metadata
# and the words used in the search box.
# -----------------------------------------

from PIL import Image
import PIL
from image_info import image_info
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,
                               QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (Slot, Qt)


class NewWindow(QWidget):
    """
    This class creates a new window. It is used to create the window which contains
    the image output. Takes a string for the file name of the image to display
    as a parameter.
    """

    def __init__(self, image):
        super().__init__()
        self.label = QLabel()
        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


def apply_filter(filter, image):
    """
    Applies the filter passed in to the image passed in. Parameters are a filter
    function and a Pillow Image object.
    """
    img_filter_manip = map(filter, image.getdata())
    image.putdata(list(img_filter_manip))


def sepia(pixel):
    """
    Applies the 'sepia' image filter to the single pixel passed in. Parameter is a 3-tuple
    of integers, treated as the color channels red, green, and blue. 
    """
    if pixel[0] < 63:
        r, g, b = int(pixel[0] * 1.1), pixel[1], int(pixel[2] * .9)
    elif pixel[0] > 62 and pixel[0] < 192:
        r, g, b = int(pixel[0] * 1.15), pixel[1], int(pixel[2] * .85)
    else:
        r = int(pixel[0] * 1.08)
        if r > 255:
            r = 255
        g, b = pixel[1], pixel[2] // 2
    return r, g, b


def grayscale(pixel):
    """
    Applies the 'grayscale' image filter to the single pixel passed in. Parameter is a 3-tuple
    of integers, treated as the color channels red, green, and blue.
    """
    return ((pixel[0] + pixel[1] + pixel[2]) // 3,) * 3


def negative(pixel):
    """
    Applies the 'negative' image filter to the single pixel passed in. Parameter is a 3-tuple
    of integers, treated as the color channels red, green, and blue.
    """
    return (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])


class MyWindow(QWidget):
    """
    Creates the main window which the user will interact with to input the search entry and their
    desired image filter. 
    """

    def __init__(self):
        super().__init__()

        self.search_label = QLabel('Search: ')
        self.search_edit = QLineEdit("Enter a search...")
        self.search_edit.setMinimumWidth(250)
        self.search_edit.selectAll()

        self.my_list = ['Sepia', 'Grayscale', 'Negative', 'Thumbnail']
        self.combo = QComboBox()
        self.combo.addItems(self.my_list)
        self.btn = QPushButton('Search')
        self._image = ""

        hbox = QHBoxLayout()
        hbox.addWidget(self.search_label)
        hbox.addWidget(self.search_edit)
        hbox.addWidget(self.combo)
        hbox.addWidget(self.btn)

        self.btn.clicked.connect(self.open_win)
        self.search_edit.returnPressed.connect(self.open_win)

        self.setLayout(hbox)
        self.setWindowTitle("Image Search")

    @Slot()
    def open_win(self):
        """
        Contains the search algorithm to find keywords in the user's search entry to determine
        which image to use to apply the filter chosen. This method calls the new window class 
        to initialize and display the new window with the image.
        """
        chosen_filter = self.combo.currentIndex()
        search_entry = self.search_edit.text().lower()

        cases_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        title_words = [[], [], [], [], [], [], [], [], [], []]

        for data in range(len(image_info)):
            _index = 0
            for word in image_info[data]["title"].split():
                title_words[data].append(word.rstrip(',').lower())
                if title_words[data][_index] in search_entry:
                    cases_counter[data] += 1
                _index += 1

            _index = 0

            for tag in range(len(image_info[data]["tags"])):
                if image_info[data]["tags"][tag].lower() in search_entry:
                    cases_counter[data] += 1

        max_value = -1
        max_index = -1
        for k in range(0, len(cases_counter)):
            if cases_counter[k] > max_value:
                max_value = cases_counter[k]
                max_index = k

        output_img_id = image_info[max_index]["id"]
        self._image = f"img/{output_img_id}.jpg"
        im = Image.open(str(self._image))
        is_thumbnail = False

        if chosen_filter == 0:
            apply_filter(sepia, im)
        elif chosen_filter == 1:
            apply_filter(grayscale, im)
        elif chosen_filter == 2:
            apply_filter(negative, im)
        else:
            is_thumbnail = True

        im = im.save("output.jpg")
        self.new_win = NewWindow("output.jpg")
        if is_thumbnail:
            self.new_win.setWindowTitle(f'Thumbnail')
        else:
            self.new_win.setWindowTitle(
                f'{self.my_list[chosen_filter]} Filter')

        self.new_win.show()
        self.repaint()


"""
Defines the variable used to hold the image pixels which will be manipulated.
Conatins the class and method calls to execute the application.
"""
img_filter_manip = []
app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
