import photo_bot
import db_session
from choose import percenting

import sys
import sqlalchemy
import json
import os

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('main_window.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))
        self.w1, self.w2, self.w3 = DoPhotoBot(), ClearPhotos(), About()

        # Если нажата кнопка "Загрузить архив", то переходим на страницу для бота
        self.gogle.clicked.connect(self.w1.show)
        self.gogle.clicked.connect(self.hide)

        # Если же нажата другая кнопка - идём на страничку для пути к архиву
        self.clear.clicked.connect(self.w2.show)
        self.clear.clicked.connect(self.hide)

        # Если нажата кнопка О проекте, то показыываем инфо
        self.about_btn.clicked.connect(self.w3.show)
        self.about_btn.clicked.connect(self.hide)


class About(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('about.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))


class DoPhotoBot(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('registrate.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))

        self.confirm.clicked.connect(self.go_bot)

    def go_bot(self):
        photo_bot.chromer(self.mail.text(), self.password.text())
        return


class ClearPhotos(QMainWindow):
    def __init__(self):
        super(ClearPhotos, self).__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('path_to_ZIP.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))

        self.confirm.clicked.connect(self.cleanning)

    def fast_clean(self, direct):
        for file in os.listdir(direct):
            if '-измененный' in file:
                os.remove(os.path.abspath(file))

    def cleanning(self):
        full_path = self.path.text()
        albums = os.listdir(full_path)
        db_sess = db_session.create_session()  # Подключаемся к базе данных
        counter = 0
        for i in albums:
            if i.startswith('Photos from'):
                path = os.path.join(full_path, i)

                os.chdir(path)  # Переходим в нужную директорию

                self.fast_clean(path)  # Чистим директорию от изменённых фото

                lstdir = sorted(os.listdir(path), key=lambda x: x[-4:])  # Формируем сортированный список файлов

                photo2 = lstdir[counter + 1]

                while photo2[-4:] != 'json':  # Пока не столкнёмся с парой jpg-json будем сравнивать соседние картинки
                    photo1, jason1 = lstdir[counter], lstdir[counter] + '.json'
                    photo2, jason2 = lstdir[counter + 1], lstdir[counter + 1] + '.json'

                    # Если объект - не фотография, то пропускаем его
                    if (photo1[-4:] != '.jpg') or (photo2[-4:] != '.jpg'):
                        counter += 1

                    # Иначе сравниваем - если сходство более 88%, то удаляем фото и json
                    elif percenting(photo1, photo2) > 88:
                        try:
                            os.remove(os.path.abspath(photo1))
                            os.remove(os.path.abspath(jason1))
                        except FileNotFoundError:
                            pass

                    else:  # Если всё хорошо, то записываем в БДшку информацию про фотографию
                        """with open(lstdir[counter + 1], 'r', encoding='utf8') as file:
                            jason = json.load(file)
                            data = Data(
                                    description=jason["description"],
                                    date=jason["photoTakenTime"]["formatted"],
                                    url=jason["url"],
                                    device=jason["googlePhotosOrigin"]["mobileUpload"]["deviceType"]
                                )
                            db_sess.add(data)
                            db_sess.commit()"""
                        counter += 2
                    lstdir = sorted(os.listdir(path))


class Data(db_session.SqlAlchemyBase):
    __tablename__ = 'Data'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    device = sqlalchemy.Column(sqlalchemy.String, nullable=True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
