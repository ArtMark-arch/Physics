import funcs
import excepts
from ui_registration import RegistrationForm
from started_form import StartForm


class MyRegistration(StartForm, RegistrationForm):

    def __init__(self):
        super().__init__()
        self.registration_button.clicked.connect(self.check_in)

    def check_in(self):
        self.login = self.login_edit.text()
        self.password = self.pass_edit.text()
        try:
            funcs.check_absence(self.login, self.password)
            check_free_login(self.login,
                             [log[0] for log in
                              self.cur.execute("""SELECT UserLogin FROM Users""").fetchall()])
            check_len(self.password)
            check_letter(self.password)
            check_digit(self.password)
            check_sequence(self.password)
            hashed_password, salt = funcs.hash_pass(self.password,
                                                    available_salt=[s[0] for s in self.cur.execute(
                                                        """SELECT UserSalt FROM Users""")])
            self.cur.execute("""INSERT INTO Users(UserLogin, UserPassword, UserSalt) VALUES(?, ?, ?)""",
                             (self.login, hashed_password, salt))
            self.con.commit()
            self.switch_window.emit("authorization")
        except excepts.AbsenceError:
            funcs.show_message("Поля должны быть заполнены!")
        except excepts.FreeLoginError:
            funcs.show_message("Логин занят!")
        except excepts.LengthError:
            funcs.show_message("Пароль должен быть длиной больше 8!")
        except excepts.LetterError:
            funcs.show_message("Пароль должен содержать символы разных регистров!")
        except excepts.DigitError:
            funcs.show_message("Пароль должен содержать цифры!")
        except excepts.SequenceError:
            funcs.show_message(
                "Пароль не должен содержать последовательность из 3 символов, подряд идущих на клавиатуре")


def check_len(password):
    """проверка длины пароля"""
    if len(password) > 8:
        return True
    raise excepts.LengthError


def check_letter(password):
    """проверка на различные регистры внутри пароля"""
    if not password.islower() and (
            not password.isupper() and not password.isdigit()):
        return True
    raise excepts.LetterError


def check_digit(password):
    """проверка на наличие цифр в пароле"""
    if set("1234567890") & set(password):
        return True
    raise excepts.DigitError


def check_sequence(password):
    """проверка на отсутствие последовательности трёх символов подряд идущих на клавиатуре"""
    alpha = ('qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'йцукенгшщзхъ',
             'фывапролджэё', 'ячсмитьбю', '1234567890')
    for s in alpha:
        for start, end in zip(range(0, len(s) - 2),
                              range(3, len(s) + 1)):
            if s[start:end] in password.lower():
                raise excepts.SequenceError
    return True


def check_free_login(login, logins):
    """проверка, что логин свободен"""
    if login not in logins:
        return True
    raise excepts.FreeLoginError
