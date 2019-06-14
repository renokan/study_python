"""
Game "Tic-tac-toe" (GUI).

Игра "Крестики-нолики".
    Условия игры:
        1. Пользователь должен выбрать игроков и нажать кнопку Start.
        2. Пользователь кликает по любому свободному полю
        3.1. Если игра с компьютером - он делает ход и показывается куда походил
        3.2. Если игра с другим игроком - он должен сделать ход
        Алгоритм повторяется пока
        А. Или заканчиваются свободные поля
        Б. Кто-то выигрывает - Вы или компьютер / второй игрок

    Особенности реализации: компьютер играет по-умному.
        1. Он первым своим ходом пытается занять центр поля.
        2. Он старается предсказать ваше выигрышное поле и занять его.
        3. Он ищет свои выигрышные поля и если такие есть - ходит туда.
"""
import tkinter as tk
from tkinter import messagebox as mb
import random


class FieldButton:
    """Это класс для полей (кнопок) с крестиками/ноликами."""

    def __init__(self, reg_field, field_num, x, y):
        """Что делаем при инициализации класса."""
        self.field_check = field_num
        self.field = tk.Button(reg_field, text='', bd=0)
        self.field.bind('<Button-1>', self.field_change)
        self.field.place(x=x, y=y, width=110, height=110)

    def field_change(self, event):
        """Функция чтобы изменить поле."""
        self.field.config(state="disabled")
        if self.field["text"] == '':
            self.field["text"] = game_noliki.xo_go
            game_noliki.msg_info.configure(text="{0} makes move {1} -> {2}".format(game_noliki.user_go, game_noliki.xo_go, self.field_check))
            self.field_check = game_noliki.xo_go
            if game_noliki.check_win():
                game_noliki.msg_result.configure(text=game_noliki.check_win())
                game_over(game_noliki.check_win())
            else:
                game_noliki.change_move()
                if game_noliki.users == 1:
                    game_noliki.comp_move()

    def field_disabled(self):
        """Функция чтобы отключить поле."""
        self.field.config(text="*")
        self.field.config(state="disabled")

    def comp_step(self):
        """Функция описывающая ход компьютера на нужное поле."""
        self.field.config(state="disabled")
        self.field["text"] = game_noliki.xo_go
        game_noliki.msg_info.configure(text="{0} makes move {1} -> {2}".format(game_noliki.user_go, game_noliki.xo_go, self.field_check))
        self.field_check = game_noliki.xo_go


class App:
    """Это класс с данными программы, если нужно будет их обнулить."""

    def __init__(self, root):
        """Что делаем при инициализации класса."""
        self.root = root
        self.app_create()
        self.app_db()
        self.add_region_start()
        self.add_canvas()
        self.add_region_info()

    def app_reset(self):
        """Обнуляем окно программы программы."""
        self.app_db()
        self.frame_start.destroy()
        self.add_region_start()
        self.reg_fields.destroy()
        self.add_canvas()
        self.frame_info.destroy()
        self.add_region_info()

    def app_db(self):
        """Данные программы."""
        self.user_go = 'You'
        self.user_wait = ''
        self.xo = ['X', 'O']
        self.xo_go = 'X'
        self.xo_wait = 'O'

    def app_create(self):
        """Конфигурируем окно программы."""
        width = 400
        height = 580
        # Название и фон
        self.root.title('Game "Tic-tac-toe"')
        self.root.configure(background='white')
        # Размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Центрируем положение
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 1.4)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.root.resizable(False, False)
        # Меню
        top_menu = tk.Menu(root)
        self.root.config(menu=top_menu)
        top_menu.add_command(label="About", command=game_info)
        top_menu.add_command(label="Reset", command=game_reset)
        top_menu.add_command(label="Exit", command=close_win)

    def add_region_start(self):
        """Выводим верхний блок - кнопка старт - программы."""
        self.frame_start = tk.Frame(self.root, width=400, height=70, bg="white")
        self.frame_start.pack()
        self.gamers = tk.IntVar()
        self.gamers.set(1)
        self.select_gm_1 = tk.Radiobutton(self.frame_start, text='You and Computer', variable=self.gamers, value=1)
        self.select_gm_2 = tk.Radiobutton(self.frame_start, text='You an other gamer', variable=self.gamers, value=2)
        self.select_gm_1.config(bg='white', highlightbackground='white', activebackground='white')
        self.select_gm_2.config(bg='white', highlightbackground='white', activebackground='white')
        self.btn_start = tk.Button(self.frame_start, text="Start game", command=self.start_game)
        self.select_gm_1.place(x=40, y=10)
        self.select_gm_2.place(x=40, y=35)
        self.btn_start.place(x=240, y=15)

    def add_canvas(self):
        """Выводим средний блок - холст - программы."""
        self.reg_fields = tk.Frame(self.root, width=400, height=400)
        self.reg_fields.pack()
        fields = tk.Canvas(self.reg_fields, width=382, height=382, bg="gray70", bd=0, highlightthickness=0)
        fields.create_line(135, 24, 135, 358)
        fields.create_line(246, 24, 246, 358)
        fields.create_line(24, 135, 358, 135)
        fields.create_line(24, 247, 358, 247)
        fields.pack()

    def add_fields(self):
        """Выводим поля-кнопки на холсте."""
        field_position = {1: (24, 24), 2: (136, 24), 3: (248, 24),
                          4: (24, 136), 5: (136, 136), 6: (248, 136),
                          7: (24, 248), 8: (136, 248), 9: (248, 248)
                          }
        self.fields_dict = {}
        for key, value in field_position.items():
            self.fields_dict[key] = FieldButton(self.reg_fields, key, value[0], value[1])

    def add_region_info(self):
        """Выводим нижний блок - инфа - программы."""
        self.frame_info = tk.Frame(self.root, width=400, height=70, bg="white")
        self.frame_info.pack()
        self.msg_rule = tk.Label(self.frame_info, bg="white", bd=10)
        self.msg_info = tk.Label(self.frame_info, bg="white", bd=0)
        self.msg_result = tk.Label(self.frame_info, bg="white", bd=10)
        self.msg_rule.pack()
        self.msg_rule.configure(text="Choose with whom you will play\nand press button 'Start game'.")
        self.msg_info.pack()
        self.msg_result.pack()

    def start_game(self):
        """Запуск программы по кнопке Старт."""
        if self.gamers.get() == 1:
            self.user_wait = 'Computer'
            self.users = 1
        else:
            self.user_wait = 'User 1'
            self.users = 2
        self.msg_rule.configure(text="Beginning of the game. You and {}.".format(self.user_wait))
        self.msg_info.configure(text="Click on the field if you want to put 'X' or 'O' there.")
        self.btn_start["state"] = "disabled"
        self.select_gm_1["state"] = "disabled"
        self.select_gm_2["state"] = "disabled"
        self.add_fields()

    def change_move(self):
        """Меняем игроков."""
        self.xo_go, self.xo_wait = self.xo_wait, self.xo_go
        self.user_go, self.user_wait = self.user_wait, self.user_go

    def free_field(self):
        """Ищем свободные поля для записи."""
        return [x.field_check for x in self.fields_dict.values() if x.field_check in range(1, 10)]

    def win_list(self):
        """Проверка выигрышных комбинаций или кол-ва свободных полей."""
        # Есть 8 выигрышных комбинаций - 3 по горизонтали, 3 по вертикали и крест
        xy = self.fields_dict  # Для краткости записи
        win_list = [[xy[1].field_check, xy[2].field_check, xy[3].field_check],
                    [xy[4].field_check, xy[5].field_check, xy[6].field_check],
                    [xy[7].field_check, xy[8].field_check, xy[9].field_check],
                    [xy[1].field_check, xy[4].field_check, xy[7].field_check],
                    [xy[2].field_check, xy[5].field_check, xy[8].field_check],
                    [xy[3].field_check, xy[6].field_check, xy[9].field_check],
                    [xy[1].field_check, xy[5].field_check, xy[9].field_check],
                    [xy[3].field_check, xy[5].field_check, xy[7].field_check]
                    ]
        return win_list

    def check_win(self):
        """Проверка выигрышных комбинаций или кол-ва свободных полей."""
        # Если есть хоть одна выигрышная комбинация, тогда...
        for win in self.win_list():
            if win.count(self.xo_go) == 3:
                for x in self.free_field():
                    self.fields_dict[x].field_disabled()
                return ("Winner {}. Game over.".format(self.user_go))

        # Если выигрышных комбинаций нет и закончились свободные ячейки, тогда...
        if len(self.free_field()) == 0:
            return ("No winner. Game over.")

    def random_field(self):
        """Случайный выбор поля компьютером."""
        return random.choice(self.free_field())

    def predict_win(self, xo=None):
        """Предсказать выигрышное поле."""
        # Перебираем список выигрышных комбинаций
        for win in self.win_list():
            # Ищем комбинацию, где уже два поля заполнены, если такое есть
            if win.count(xo) == 2:
                for x in win:
                    # Ищем цифру и выводим её
                    if isinstance(x, int):
                        return x

    def effective_step(self):
        """Стараемся делать эффективные ходы, хотя и рандомайзом."""
        free_fields = self.free_field()
        if len(free_fields) > 7:
            # Компьютеру нужно сделать свой первый ход, стараемся занять центр
            if 5 in free_fields:
                return 5
            else:
                return self.random_field()
        elif len(free_fields) > 5:
            # Компьютеру нужно сделать второй ход
            # 1. Пробуем мешать сопернику, предсказав его выигрышное поле
            # 2. Если такого нет - делаем случайный ход
            if self.predict_win(self.xo_wait):
                return self.predict_win(self.xo_wait)
            else:
                return self.random_field()
        else:
            # Компьютеру нужно сделать остальные ходы
            # 1. Ищем своё выигрышное поле
            # 2. Пробуем мешать сопернику, предсказав его выигрышное поле
            # 3. Если такого нет - делаем случайный ход
            if self.predict_win(self.xo_go):
                return self.predict_win(self.xo_go)
            elif self.predict_win(self.xo_wait):
                return self.predict_win(self.xo_wait)
            else:
                return self.random_field()

    def comp_move(self):
        """Выбираем куда компьютеру ходить."""
        self.fields_dict[self.effective_step()].comp_step()
        if self.check_win():
            self.msg_result.configure(text=self.check_win())
            game_over(self.check_win())
        else:
            self.change_move()


def game_info():
    """Показываем информацию об игре."""
    output = "\nChoose with whom you will play and press button 'Start game'.\n"
    output += "\nClick on the field if you want to put 'X' or 'O' there.\n"
    mb.showinfo(title="About", message=output)


def game_over(info):
    """Показываем информацию о завершении игры."""
    mb.showinfo(title="Result", message=info)


def game_reset():
    """Сброс игры."""
    answer = mb.askyesno(title="Reset", message="Reset the game?")
    if answer is True:
        App.app_reset(game_noliki)


def close_win():
    """Корректное закрытие окна программы."""
    answer = mb.askyesno(title="Exit", message="Close the program?")
    if answer is True:
        root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    game_noliki = App(root)
    root.mainloop()
