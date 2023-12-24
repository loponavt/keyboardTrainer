import sys
import time
from threading import Thread

from PySide2.QtGui import *
from PySide2.QtWidgets import *

import requests

session = requests.Session()
base_url = "https://fish-text.ru/get"
response = session.get(url=base_url)
input_text = (response.json()["text"])

# input_text = "disc jockey more commonly abbreviated person who plays recorded music for an audience " \
#              "types include radio who host programs music radio stations club work nightclub " \
#              "music festival mobile hired work public private events such weddings parties " \
#              "festivals turntablists use record players manipulate sounds phonograph " \
#              "records originally disc jockey referred shellac later vinyl records nowadays" \
#              "used encompassing term also describe persons mix music from other recording media such " \
#              "cassettes digital audio files controller even laptop may adopt title" \
#              "front their real names adopted pseudonyms stage names"


class MainWindow(QDialog):
    def __init__(self, parent=None):
        self.char_total = 0
        self.char_correctly = 0
        self.speed = 0

        self.timer_thread = Thread(target=self.timer_count, daemon=True)

        super(MainWindow, self).__init__(parent)
        self.layout = QGridLayout()
        self.title = 'KeyboardTrainer'
        self.left = 200
        self.top = 200
        self.width = 1500
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        self.text_to_print = QTextEdit(input_text)
        self.text_to_print.setReadOnly(True)

        self.lb_chars_correctly = QLabel("Правильно введено: ")
        self.lb_speed = QLabel("Скорость ввода:")

        self.input_text = QLineEdit()
        self.input_text.setMinimumHeight(100)

        self.layout.addWidget(self.text_to_print, 1, 0, 1, 2)
        self.layout.addWidget(self.lb_chars_correctly, 2, 0)
        self.layout.addWidget(self.lb_speed, 2, 1)
        self.layout.addWidget(self.input_text, 3, 0, 1, 2)
        self.setLayout(self.layout)

        # шрифт
        self.font = self.text_to_print.font()
        self.font.setPointSize(14)
        self.lb_speed.setFont(self.font)
        self.lb_chars_correctly.setFont(self.font)
        self.text_to_print.setFont(self.font)
        self.input_text.setFont(self.font)

        self.flag = False
        self.input_text.cursorPositionChanged.connect(self.cursor_position_changed)

    def timer_count(self):
        start = time.time()
        while True:
            now = time.time()
            time_passed = now - start
            if time_passed == 0:
                time.sleep(1)
                continue
            self.lb_speed.setText("Скорость ввода: " + str(round(self.char_total / time_passed, 1) * 60)[:-2])
            time.sleep(1)

    def cursor_position_changed(self):
        cursor_position = self.input_text.cursorPosition() - 1
        try:
            if input_text[cursor_position] == self.input_text.text()[cursor_position]:
                self.char_correctly += 1
                self.change_color(self.text_to_print, cursor_position, "green")
            else:
                self.change_color(self.text_to_print, cursor_position, "red")
        except IndexError:
            print("gotcha")

    def change_color(self, text, index, color):
        if not self.flag:
            self.timer_thread.start()
            self.flag = True

        cursor = QTextCursor(text.document())
        cursor.setPosition(index)

        char_format = QTextCharFormat()
        char_format.setForeground(QColor(color))

        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(char_format)
        cursor.setPosition(index)
        self.text_to_print.setTextCursor(cursor)
        self.char_total += 1
        self.lb_chars_correctly.setText(
            "Правильно введено: " + str(round(self.char_correctly / self.char_total * 100, 0))[:-2] + "%")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())