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
        return


class ClearPhotos(QMainWindow):
    def __init__(self):
        super(ClearPhotos, self).__init__()
        # Создаём оболочку и подключаем кнопки
        uic.loadUi('path_to_ZIP.ui', self)
        self.logo.setPixmap(QPixmap('logo.png'))

        self.confirm.clicked.connect(self.cleanning)

    def cleanning(self):
        full_path = self.path.text()
        albums = os.listdir(full_path)
        #db_sess = db_session.create_session()  # Подключаемся к базе данных
        counter = 0
        for i in albums:
            if i.startswith('Photos from'):
                path = full_path + f'\\{i}'
                os.chdir(path)
                a = os.listdir(path)
                print(a)
                while counter <= len(a) - 3:
                    photo1, jason1 = a[counter], a[counter + 1]
                    photo2, jason2 = a[counter + 2], a[counter + 3]

                    # Если объект - не фотография, то пропускаем его и его json
                    if photo1[-4:] != '.jpg':
                        counter += 2

                    # Иначе сравниваем - если сходство более 88%, то удаляем фото и json
                    elif percenting(photo1, photo2) > 88:
                        os.remove(os.path.abspath(photo1))

                    else:  # Если всё хорошо, то записываем в БДшку информацию про фотографию
                        """with open(a[counter + 1], 'r', encoding='utf8') as file:
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
                    os.remove(os.path.abspath(jason1))


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
