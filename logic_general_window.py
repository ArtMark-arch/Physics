import sqlite3
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog
from general import Ui_General
from funcs import show_message
from excepts import EmptyValueError
from excepts import AvailableValueError
from excepts import BadTimeError
from excepts import NotPickError

COLUMNS = 1
MOVES = "Moves"
BODIES = "Bodies"


class MyGeneralWindow(QMainWindow, Ui_General):

    def __init__(self, login):
        super().__init__()
        self.setupUi(self)
        self.login = login
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.user_id = self.cur.execute("""SELECT UserId FROM Users
                                                WHERE UserLogin = ?""", (self.login,)).fetchone()[0]
        self.table_status = MOVES  # таблица, отображаемая tableWidget
        self.create_btn.clicked.connect(self.new)
        self.clear_btn.clicked.connect(self.clean_out)
        self.delete_btn.clicked.connect(self.remove)
        self.tableWidget.itemDoubleClicked.connect(self.switch)
        self.tableWidget.itemClicked.connect(self.item_clicked)
        self.move_id = None
        self.body_id = None
        self.my_update()
        self.back_to_moves.hide()
        self.back_to_moves.clicked.connect(self.switch)
        self.curr_body_title.hide()
        self.curr_move_title.hide()
        self.on_gr_btn.clicked.connect(self.set_graphic)

    def switch(self):
        if self.table_status == MOVES:
            self.table_status = BODIES
            self.tableWidget.itemDoubleClicked.disconnect(self.switch)
        else:
            self.table_status = MOVES
            self.tableWidget.itemDoubleClicked.connect(self.switch)
            self.back_to_moves.hide()
            self.curr_body_title.hide()
            self.curr_move_title.hide()
        self.my_update()

    def item_clicked(self, item):
        if self.table_status == MOVES:
            self.move_id = self.cur.execute("""SELECT MoveId FROM Moves
                                                WHERE MoveTitle = ?""", (item.text(),)).fetchone()[0]
            self.curr_move_title.show()
            self.curr_move_title.setText(f"выбрано движение: {item.text()}")
        else:
            self.body_id = self.cur.execute("""SELECT BodyId FROM Bodies
                                                WHERE BodyTitle = ?""", (item.text(),)).fetchone()[0]
            self.curr_body_title.show()
            self.curr_body_title.setText(f"выбрано тело: {item.text()}")
            values = self.cur.execute(f"""SELECT BodyFirSpeed, BodyAcceleration, BodyTime FROM Bodies
                                            WHERE BodyId = {self.body_id}""").fetchall()[0]
            self.graphicsView.clear()
            self.fir_speed_edit.clear()
            self.acceleration_edit.clear()
            self.time_edit.clear()
            if len(values) == 3 and all(values):
                self.fir_speed_edit.setText(str(values[0]))
                self.acceleration_edit.setText(str(values[1]))
                self.time_edit.setText(str(values[2]))
        self.my_update()

    def my_update(self):
        moves = [move[0::2] for move in self.cur.execute(f"""SELECT * FROM Moves
                                     WHERE UserId = ?""", (self.user_id,)).fetchall()]
        bodies = [body[2] for body in self.cur.execute(f"""SELECT * FROM Bodies
                                     WHERE MoveId = ?""", (self.move_id,))]
        if self.table_status == MOVES:
            result = moves
            title = "MoveTitle"
            if not moves:
                self.curr_move_title.hide()
        else:
            if not bodies:
                self.curr_body_title.hide()
            self.back_to_moves.show()
            result = bodies
            title = "BodyTitle"
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(COLUMNS)
        self.tableWidget.setHorizontalHeaderLabels([title])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem[1] if result == moves else elem)))

    def new(self):
        if self.table_status == MOVES:
            pair = QInputDialog.getText(self, "Введите название движения", "Как назвать новое движение?")
            while pair[0] in [x[0] for x in
                              self.cur.execute("""SELECT MoveTitle FROM 
                              Moves WHERE UserId = ?""", (self.user_id,)).fetchall()] or not pair[0]:
                show_message("Движение с таким названием уже есть!")
                pair = QInputDialog.getText(self, "Введите название движения",
                                            "Как назвать новое движение?")
            self.cur.execute(
                f"""INSERT INTO Moves(UserId,MoveTitle) VALUES({self.user_id},'{pair[0]}') """)
        else:
            pair = QInputDialog.getText(self, "Введите название тела", "Как назвать новое тело?")
            while pair[0] in [x[0] for x in
                              self.cur.execute("""SELECT BodyTitle FROM Bodies""").fetchall()]:
                show_message("Тело с таким названием уже есть!")
                pair = QInputDialog.getText(self, "Введите название тела", "Как назвать новое тело?")
            self.cur.execute(
                f"""INSERT INTO Bodies(MoveId,BodyTitle) VALUES({self.move_id},'{pair[0]}') """)
        self.my_update()

    def remove(self):
        if self.table_status == MOVES:
            self.cur.execute(f"""DELETE from Moves
                                where MoveId = {self.move_id}""")
        else:
            self.cur.execute(f"""DELETE from Bodies
                                where BodyId = {self.body_id}""")
        self.my_update()

    def clean_out(self):
        if self.table_status == MOVES:
            self.cur.execute(f"""DELETE from Bodies
                                 where MoveId = {self.move_id}""")
        else:
            self.cur.execute(f"""UPDATE Bodies
                                 SET BodyFirSpeed = 0,
                                 BodyAcceleration = 0, BodyTime = 0 where BodyId = {self.body_id}""")

    def set_graphic(self):
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
                                 BodyTime = {time} where BodyId = {self.body_id}""")
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
        if self.body_id:
            return True
        raise NotPickError

    def closeEvent(self, event):
        self.con.commit()
        self.con.close()


def check_not_empty_values(*values):
    for value in values:
        if not value:
            raise EmptyValueError
    return True


def check_good_time(time):
    if time <= 0:
        raise BadTimeError
    return True
