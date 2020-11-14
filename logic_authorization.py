import excepts
import funcs
from ui_authorization import AuthorizationForm
from started_form import StartForm


class MyAuthorization(StartForm, AuthorizationForm):

    def __init__(self):
        super().__init__()
        self.login_button.clicked.connect(self.check_in)
        self.registration_button.clicked.connect(self.registration)

    def check_in(self):
        """Ввод логина и пароля, проверка, сигнал о смене окна на основное, иначе ошибка"""
        self.login = self.login_edit.text()
        self.password = self.pass_edit.text()
        try:
            funcs.check_absence(self.login, self.password)
            logins = [log[0] for log in self.cur.execute("""SELECT UserLogin FROM Users""").fetchall()]
            if self.login in logins:
                hashed_pass = \
                    self.cur.execute("""SELECT UserPassword FROM Users WHERE UserLogin = ?""",
                                     (self.login,)).fetchone()[0]
                salt = self.cur.execute("""SELECT UserSalt FROM Users WHERE UserLogin = ?""",
                                        (self.login,)).fetchone()[0]
                if funcs.hash_pass(self.password, salt=salt) != hashed_pass:
                    raise excepts.BadDataError
            else:
                raise excepts.BadDataError
            self.switch_window.emit("general")
        except excepts.AbsenceError:
            funcs.show_message("Поля должны быть заполнены!")
        except excepts.BadDataError:
            funcs.show_message("Неверный логин или пароль!")

    def registration(self):
        """сигнал о смене окна на регистрацию"""
        self.switch_window.emit("registration")
