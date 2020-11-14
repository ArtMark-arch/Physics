import sys
from PyQt5.QtWidgets import QApplication
from logic_authorization import MyAuthorization
from logic_registration import MyRegistration
from logic_general_window import MyGeneralWindow


class Controller:

    def __init__(self):
        self.windows = {"authorization": MyAuthorization(), "registration": MyRegistration()}
        self.windows["authorization"].switch_window.connect(self.show_window)
        self.windows["registration"].switch_window.connect(self.show_window)

    def show_window(self, title):
        """Отвечает за показ окон"""
        if title == "general":
            self.windows["general"] = MyGeneralWindow(self.windows["authorization"].login)
        self.windows[title].show()
        self.clear_windows(title)

    def clear_windows(self, title):
        """Скрывает окна с названием отличным от title"""
        for window in self.windows:
            if window != title:
                self.windows[window].hide()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_window("authorization")
    sys.excepthook = except_hook
    sys.exit(app.exec())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    main()
