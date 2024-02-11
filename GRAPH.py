import sys
import os

import numpy as np
import numexpr as ne

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyqtgraph as pg
import pyqtgraph.exporters

# from ui import Ui_Form

grapics = []


class StartWin(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('StartWindow.ui', self)

        self.GoButton.clicked.connect(self.switchGraph)

    def switchGraph(self):
        if self.BlackBtn.isChecked():
            color = 'b'
        else:
            color = 'w'

        name = self.NameText.toPlainText()
        if name == '':
            name = ' '

        with open("name+color.txt", "a+") as my_file:
            my_file.write('@')
            my_file.write(color)
            my_file.write('$')
            my_file.write(name)

        global grapics
        grapics = []
        exGr.show()


class GraphWin(QMainWindow):
    def __init__(self):
        super().__init__()
        global grapics

        uic.loadUi('GraphWindow.ui', self)  # Загружаем дизайн

        self.Field.showGrid(x=True, y=True)

        self.SaveBtn.triggered.connect(self.SaveImage)
        self.SaveBtn.setShortcut(QKeySequence("Ctrl+S"))

        self.AddButton.clicked.connect(self.Add)




    def SaveImage(self):
        exporter = pg.exporters.ImageExporter(self.Field.scene())
        path = str(os.getcwd())
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image",
                                                  f"{path}",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        exporter.export(filePath)
        exSaved.show()

    def draw(self, mas):
        # print(mas)
        self.Field.showGrid(x=True, y=True)
        grapics.append(mas)
        print(grapics)

    def event(self, event, **kwargs):
        if event.type() == QEvent.WindowActivate:
            self.coltitle()
            print(65, grapics)

            for mas in grapics:
                e = mas[0]
                x = list(np.arange(mas[1], mas[2] + 1))
                y = list(ne.evaluate(e))
                print(x, y)
                # self.Field.setBackground("w")
                self.Field.plot(x, y, pen=mas[3], width=79)
                print(mas)

        return QWidget.event(self, event)

    def coltitle(self):
        with open("name+color.txt", "r+") as my_file:
            x = my_file.read().split('@')[-1]
            x = x.split('$')
            color = x[0]
            title = x[1]
        self.Title.setText(title)
        if color == 'w':
            self.Field.setBackground("w")
        else:
            self.Field.setBackground("k")

    def Add(self):
        exAdd.show()


class AddWin(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddGraphWindow.ui', self)  # Загружаем дизайн

        self.OKButton.clicked.connect(self.add_OK)
        self.CancelButton.clicked.connect(self.close_Cancel)

    def add_OK(self):
        colors = {'Красный': 'r', 'Зелёный': 'g', 'Синий': 'b', 'Чёрный': 'k', 'Фиолетовый': 'violet',
                  'Оранжевый': 'orange', 'Розовый': 'pink', 'Голубой': 'cyan', 'Белый': 'white'}
        equal = self.finctionTE.toPlainText()
        left_limit = self.lineEditFROM.text()
        if left_limit == '':
            left_limit = -100
        left_limit = int(left_limit)
        right_limit = self.lineEditTO.text()
        if right_limit == '':
            right_limit = 100
        right_limit = int(right_limit)
        color = colors[self.colorBox.currentText()]
        print(color)
        mas = [equal, left_limit, right_limit, color]
        GraphWin.draw(GraphWin(), mas)
        exAdd.close()

    def close_Cancel(self):
        exAdd.close()


class SavedFile(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('SavedFile.ui', self)

        self.OK.clicked.connect(self.dOK)
        self.Exit.clicked.connect(self.exit())

    def dOK(self):
        exSaved.close()

    def exit(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWin()  # Стартовое окно (класс)
    exGr = GraphWin()  # Основное окно (класс)
    exAdd = AddWin()
    exSaved = SavedFile()
    ex.show()  # Изначально - открытие стартового окна
    sys.exit(app.exec_())
