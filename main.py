import photo_bot
from choose import percenting

import sys
import sqlalchemy

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('main_window.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))
        self.w1, self.w2 = DoPhotoBot(), ClearPhotos()

        # Если нажата кнопка "Загрузить архив", то переходим на страницу для бота
        self.gogle.clicked.connect(self.w1.show)
        self.gogle.clicked.connect(self.hide)

        # Если же нажата другая кнопка - идём на страничку для пути к архиву
        self.clear.clicked.connect(self.w2.show)
        self.clear.clicked.connect(self.hide)


class DoPhotoBot(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('registrate.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))

        self.confirm.clicked.connect(self.go_bot)

    def go_bot(self):
        photo_bot.chromer(self.mail.text(), self.password.text())


class ClearPhotos(QMainWindow):
    def __init__(self):
        super(ClearPhotos, self).__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('path_to_ZIP.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))

        self.confirm.clicked.connect(self.cleanning)

    def cleanning(self):
        a = self.path.text()
        counter = 0
        while counter <= len(a) - 3:
            photo1, jason1 = a[counter], a[counter + 1]
            photo2, jason2 = a[counter + 2], a[counter + 3]
            if percenting(photo1, photo2) > 88:
                del a[counter:counter + 1]
            else:
                with open(a[counter + 1], 'r', encoding='utf8') as file:
                    jason = file.read()
                    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
                    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
                    device = sqlalchemy.Column(sqlalchemy.String, nullable=True)

                counter += 2


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
