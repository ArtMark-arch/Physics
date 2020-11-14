import sqlite3

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog

from excepts import NotPickError, EmptyValueError, BadTimeError, AvailableValueError
from funcs import show_message
from general import Ui_General

COLUMNS = 1
MOVES = "Move", "Moves"
BODIES = "Body", "Bodies"


class MyGeneralWindow(QMainWindow, Ui_General):

    def __init__(self, login):
        super().__init__()
        self.setupUi(self)
        self.curr_move_title.hide()
        self.curr_body_title.hide()
        self.back_to_moves.hide()
        self.gr_label.hide()
        self.create_btn.clicked.connect(self.new)
        self.clear_btn.clicked.connect(self.clean)
        self.delete_btn.clicked.connect(self.delete)
        self.back_to_moves.clicked.connect(self.switch)
        self.on_gr_btn.clicked.connect(self.set_gr)
        self.tableWidget.cellClicked.connect(self.pick)
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.user_id = self.cur.execute("""SELECT UserId FROM Users
            WHERE UserLogin = ?""", (login,)).fetchone()[0]
        self.table_status = MOVES  # изначально таблица отображает движения пользователя
        self.picked_move = ()
        self.picked_body = ()
        self.my_update()

    def switch(self):
        if self.table_status == MOVES:
            self.table_status = BODIES
        else:
            self.picked_move = ()
            self.table_status = MOVES
        self.picked_body = ()
        self.my_update()

    def pick(self):
        """Выбирает текущее движение или тело"""
        if self.table_status == MOVES:
            self.picked_move = self.cur.execute("""SELECT * FROM Moves
                                                    WHERE MoveTitle = ?""",
                                                (self.tableWidget.currentItem().text(),)).fetchone()
        elif self.table_status == BODIES and self.picked_move:
            self.picked_body = self.cur.execute("""SELECT * FROM Bodies
                                                WHERE BodyTitle = ?""",
                                                (self.tableWidget.currentItem().text(),)).fetchone()
            if self.picked_body[3]:
                self.fir_speed_edit.setText(str(self.picked_body[3]))
            if self.picked_body[4]:
                self.acceleration_edit.setText(str(self.picked_body[4]))
            if self.picked_body[5]:
                self.time_edit.setText(str(self.picked_body[5]))
        self.my_update()
        if self.table_status == BODIES and self.picked_move and not any(self.picked_body[3:]):
            self.clean()

    def my_update(self):
        """Сохраняет изменения, обновляет состояние виджетов: таблицы, марок выбранных объектов, графика."""
        self.con.commit()
        if self.picked_move and self.picked_move[0] in [move[0] for move in self.cur.execute(
                "SELECT MoveId FROM Moves").fetchall()]:
            self.gr_label.hide()
            self.curr_move_title.show()
            self.curr_move_title.setText(f"Выбрано движение: {self.picked_move[2]}")
            self.back_to_moves.show()
        else:
            self.curr_move_title.hide()
            self.back_to_moves.hide()
            self.picked_move = ()
        if self.picked_body and self.picked_body[0] in [body[0] for body in self.cur.execute(
                "SELECT BodyId FROM Bodies").fetchall()]:
            self.curr_body_title.show()
            self.curr_body_title.setText(f"Выбрано тело: {self.picked_body[2]}")
            self.gr_label.show()
        else:
            self.curr_body_title.hide()
            self.gr_label.hide()
            self.picked_body = ()
        if not (self.picked_move or self.picked_body):
            self.back_to_moves.hide()
        if self.table_status == MOVES:
            self.clear_btn.hide()
            self.fir_speed_edit.hide()
            self.fir_speed_label.hide()
            self.acceleration_edit.hide()
            self.acceleration_label.hide()
            self.time_edit.hide()
            self.time_label.hide()
            self.on_gr_btn.hide()
            result = [move[0::2] for move in self.cur.execute(f"""SELECT * FROM Moves
                                     WHERE UserId = ?""", (self.user_id,)).fetchall()]
            title = "MoveTitle"
        else:
            self.clear_btn.show()
            self.fir_speed_edit.show()
            self.fir_speed_label.show()
            self.acceleration_edit.show()
            self.acceleration_label.show()
            self.time_edit.show()
            self.time_label.show()
            self.on_gr_btn.show()
            result = [body[2] for body in self.cur.execute(f"""SELECT * FROM Bodies
                                     WHERE MoveId = ?""", (self.picked_move[0],))]
            title = "BodyTitle"
        self.graphicsView.clear()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(COLUMNS)
        self.tableWidget.setHorizontalHeaderLabels([title])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(
                    str(elem[1] if self.table_status == MOVES else elem)))

    def new(self):
        """Создаёт новое движение/тело"""
        good_title = None
        ok_pressed = True
        moves = [move[2] for move in self.cur.execute("""SELECT * FROM Moves WHERE UserId = ?""",
                                                      (self.user_id,)).fetchall()]
        bodies = [x[2] for x in self.cur.execute("""SELECT * FROM Bodies""").fetchall()]
        if self.table_status == MOVES:
            error_msg = "Движение с таким названием уже есть!"
            win_title = "Введите название движения"
            prompt = "Как назвать новое движение?"
        else:
            error_msg = "Тело с таким названием уже есть!"
            win_title = "Введите название тела"
            prompt = "Как назвать новое тело?"
        title = ""
        while not good_title and ok_pressed:
            if good_title is None:
                good_title = False
            else:
                show_message(error_msg)
            title, ok_pressed = QInputDialog.getText(self, win_title, prompt)
            if title not in (moves if self.table_status == MOVES else bodies):
                good_title = True
        if ok_pressed and title:
            if self.table_status == MOVES:
                self.cur.execute(
                    f"""INSERT INTO Moves(UserId,MoveTitle) VALUES({self.user_id},'{title}') """)
            else:
                self.cur.execute(
                    f"""INSERT INTO Bodies(MoveId,BodyTitle) VALUES({self.picked_move[0]},'{title}') """)
            self.my_update()

    def clean(self):
        """Очищает данные выбранного тела"""
        if self.picked_body:
            self.cur.execute(
                f"""UPDATE Bodies SET BodyFirSpeed = 0, BodyAcceleration = 0, BodyTime = 0 where BodyId = 
                        {self.picked_body[0]}""")
            self.fir_speed_edit.clear()
            self.acceleration_edit.clear()
            self.time_edit.clear()
            self.graphicsView.clear()
        else:
            show_message("Выберите тело!")

    def delete(self):
        """Удаляет движение/тело"""
        if self.table_status == MOVES:
            if self.picked_move:
                self.cur.execute(f"""DELETE from Moves where MoveId = {self.picked_move[0]}""")
            else:
                show_message("Выберите движение!")
        else:
            if self.picked_body:
                self.cur.execute(f"""DELETE from Bodies where BodyId = {self.picked_body[0]}""")
            else:
                show_message("Выберите тело!")
        self.my_update()

    def set_gr(self):
        """установка состояния выбранного тела на график"""
        speed = self.fir_speed_edit.text()
        acceleration = self.acceleration_edit.text()
        time = self.time_edit.text()
        try:
            self.check_have_body()
            check_not_empty_values(speed, acceleration, time)
            speed = int(speed)
            acceleration = int(acceleration)
            time = int(time)
            check_good_time(time)
            speeds = [speed + acceleration * t for t in range(time + 1)]
            self.graphicsView.clear()
            self.graphicsView.plot([t for t in range(time + 1)], speeds, pen="r")
            self.cur.execute(f"""UPDATE Bodies
                                         SET BodyFirSpeed = {speed}, BodyAcceleration = {acceleration},
                                         BodyTime = {time} where BodyId = {self.picked_body[0]}""")
        except ValueError:
            show_message("Значения должны быть целыми числами!")
        except NotPickError:
            show_message("Должно быть выбрано тело!")
        except AvailableValueError:
            show_message("Недоступное значение!")
        except EmptyValueError:
            show_message("Пустое значение!")
        except BadTimeError:
            show_message("Путешествие назад во времени?")

    def check_have_body(self):
        """Проверка на то, что тело выбрано"""
        if self.picked_body:
            return True
        raise NotPickError

    def closeEvent(self, event):
        self.con.commit()
        self.con.close()


def check_not_empty_values(*values):
    """Проверяет, что значения не пустые"""
    for value in values:
        if not value:
            raise EmptyValueError
    return True


def check_good_time(time):
    """Проверяет, что время положительно"""
    if time <= 0:
        raise BadTimeError
    return True
