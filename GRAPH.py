import os
import sys

import numpy as np
import numexpr as ne

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pyqtgraph as pg
import pyqtgraph.exporters

grapics = []  # список всех добавленных графиков


class StartWin(QDialog):  # стартовое окно
    def __init__(self):
        super().__init__()
        uic.loadUi('StartWindow.ui', self)

        self.GoButton.clicked.connect(self.switchGraph)

    def switchGraph(self):  # переключение окон
        if self.BlackBtn.isChecked():
            color = 'b'
        else:
            color = 'w'

        name = self.NameText.toPlainText()  # получение текста, введённого пользователем
        if name == '':
            name = ' '

        with open("name+color.txt", "a+") as my_file:  # запись данных, введённых пользователем в текстовый файл
            my_file.write('@')
            my_file.write(color)
            my_file.write('$')
            my_file.write(name)

        global grapics
        grapics = []
        exGr.show()  # показ следующего окна


class GraphWin(QMainWindow):  # основное окно
    def __init__(self):
        super().__init__()
        global grapics

        uic.loadUi('GraphWindow.ui', self)  # Загружаем дизайн

        self.Field.showGrid(x=True, y=True)  # показ сетки на поле

        self.SaveBtn.triggered.connect(self.SaveImage)  # подключение кнопок
        self.SaveBtn.setShortcut(QKeySequence("Ctrl+S"))

        self.HelpBtn.triggered.connect(self.HelpOpen)
        self.HelpBtn.setShortcut(QKeySequence("Ctrl+H"))

        self.AddButton.clicked.connect(self.Add)

    def SaveImage(self):  # функция для сохранения рисунка
        exporter = pg.exporters.ImageExporter(self.Field.scene())
        path = str(os.getcwd())  # получение пути к текущей папке
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image",  # открытие диалогового окна для сохранения файла
                                                  f"{path}",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        exporter.export(filePath)  # экспорт поля с графиками
        exSaved.show()  # показ следующего окна

    def HelpOpen(self):  # открыть файл с руководством пользователя
        pass

    def draw(self, mas):  # добавить полученные данные для отрисовки графика в общий массив
        # print(mas)
        self.Field.showGrid(x=True, y=True)
        grapics.append(mas)
        # print(grapics)

    def event(self, event, **kwargs):  # проверка текущего события
        if event.type() == QEvent.WindowActivate:  # если окно активировано
            self.color_title()  # вызываем функцию для добавления заголовка и фонового цвета

            for mas in grapics:  # отрисовываем каждый график из массива
                e = mas[0]
                x = list(np.arange(mas[1], mas[2] + 1))
                y = list(ne.evaluate(e))
                # print(x, y)
                # self.Field.setBackground("w")
                self.Field.plot(x, y, pen=mas[3], width=79)
                # print(mas)

        return QWidget.event(self, event)

    def color_title(self):  # добавление цвета фона и заголовка
        with open("name+color.txt", "r+") as my_file:  # считываем введённые пользователем данные из текстового файла
            x = my_file.read().split('@')[-1]
            x = x.split('$')
            color = x[0]
            title = x[1]
        self.Title.setText(title)  # устанавливаем заголовок
        if color == 'w':
            self.Field.setBackground("w")  # устанавливаем фон
        else:
            self.Field.setBackground("k")

    def Add(self):  # функция для показа следующего окна при нажатии на кнопку
        exAdd.show()


class AddWin(QDialog):  # окно добавления графика
    def __init__(self):
        super().__init__()
        uic.loadUi('AddGraphWindow.ui', self)  # загружаем дизайн

        self.OKButton.clicked.connect(self.add_OK)  # подключение кнопок
        self.CancelButton.clicked.connect(self.close_Cancel)

    def add_OK(self):  # функция получения данных, введённых пользователем (если нажата кнопка ОК)
        colors = {'Красный': 'r', 'Зелёный': 'g', 'Синий': 'b', 'Чёрный': 'k', 'Фиолетовый': 'violet',
                  'Оранжевый': 'orange', 'Розовый': 'pink', 'Голубой': 'cyan', 'Белый': 'white'}
        equal = self.finctionTE.toPlainText()  # заданная функция
        left_limit = self.lineEditFROM.text()
        if left_limit == '':
            left_limit = -100
        left_limit = int(left_limit)
        right_limit = self.lineEditTO.text()
        if right_limit == '':
            right_limit = 100
        right_limit = int(right_limit)
        color = colors[self.colorBox.currentText()]
        # print(color)
        mas = [equal, left_limit, right_limit, color]  # создаем массив всех параметров этого графика
        GraphWin.draw(GraphWin(), mas)  # вызываем функцию другого класса для добавления графика в общий массив
        exAdd.close()  # закрываем окно

    def close_Cancel(self):  # если нажата кнопка Cancel
        exAdd.close()  # закрываем окно


class SavedFile(QDialog):  # окно: "Файл успешно сохранен"
    def __init__(self):
        super().__init__()
        uic.loadUi('SavedFile.ui', self)

        self.OK.clicked.connect(self.func_OK)  # подключение кнопок
        self.Exit.clicked.connect(self.func_exit)

    def func_OK(self):  # если ОК - закрытие данного окна, возврат к основному окну
        exSaved.close()

    def func_exit(self):  # если ВЫХОД - возврат на начальный экран
        exGr.close()
        exSaved.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWin()  # Стартовое окно (класс)
    exGr = GraphWin()  # Основное окно (класс)
    exAdd = AddWin()  # Окно добавления графиков (класс)
    exSaved = SavedFile()  # окно: "Файл успешно сохранен" (класс)
    ex.show()  # Изначально - открытие стартового окна
    sys.exit(app.exec_())
