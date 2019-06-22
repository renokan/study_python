"""Game "Sudoku"."""
import tkinter as tk
from tkinter import messagebox as mb


class FieldEntry:
    """Это класс полей (тип Entry) для ввода цифр."""

    def __init__(self, reg_field, f_xy, f_num, f_row, f_col, f_group):
        """Что делаем при инициализации класса."""
        self.num_field = f_num
        self.num_row = f_row
        self.num_col = f_col
        self.num_group = f_group
        self.field_get = ''
        self.field_search = [x for x in range(1, 10)]
        self.field = tk.Entry(reg_field, bd=1, bg='white', justify="center")
        self.field.bind('<FocusOut>', self.check_get)
        self.field.place(x=f_xy[0], y=f_xy[1], width=48, height=48)

        # self.field.insert(0, self.num_field)
        # self.field.insert(0, self.num_group)

    def field_insert(self, num_insert):
        """Записываем число в нужное поле."""
        self.field.delete(0, "end")
        self.field.insert(0, num_insert)

    def check_get(self, event):
        """Проверяем заполнение полей."""
        try:
            # Пробуем введенный параметр привести к целому числу
            x = int(self.field.get())
        except ValueError:
            # Если тип не подходящий
            self.field_get = ''
            self.field.delete(0, "end")
            self.field.configure(bg='white')
            # Проверяем кол-во
            sudoku.selected_fields()
        else:
            # Если получилось число, проверяем на соответствие диапазону
            if x in range(1, 10):
                self.field_get = x
                self.field.configure(bg='lightgrey')
            else:
                self.field_get = ''
                self.field.delete(0, "end")
                self.field.configure(bg='white')
            # Проверяем кол-во
            sudoku.selected_fields()


class App:
    """Это класс с данными программы, если нужно будет их обнулить."""

    def __init__(self, root):
        """Что делаем при инициализации класса."""
        self.root = root
        self.app_create()
        self.app_db()
        self.add_canvas()
        self.add_region_start()
        self.add_region_info()

    def app_reset(self):
        """Обнуляем окно программы программы."""
        self.app_db()
        self.frame_fields.destroy()
        self.add_canvas()
        self.frame_start.destroy()
        self.add_region_start()
        self.frame_info.destroy()
        self.add_region_info()

    def app_db(self):
        """Данные программы."""
        pass

    def app_create(self):
        """Конфигурируем окно программы."""
        width = 480
        height = 600
        # Название и фон
        self.root.title('Game "Sudoku"')
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
        top_menu = tk.Menu(self.root)
        self.root.config(menu=top_menu)
        top_menu.add_command(label="About", command=game_info)
        top_menu.add_command(label="Reset", command=game_reset)
        top_menu.add_command(label="Exit", command=game_exit)

        line = tk.Frame(self.root, width=480, height=8, bg="white")
        line.pack()

    def add_canvas(self):
        """Выводим блок - холст - программы."""
        self.frame_fields = tk.Frame(self.root, width=480, height=480)
        self.frame_fields.pack()
        fields = tk.Canvas(self.frame_fields, width=464, height=464, bg="gray70", bd=0, highlightthickness=0)
        fields.create_rectangle(1, 1, 463, 463, width=2)
        pos_line = [53, 104, 207, 258, 361, 412]
        for y in pos_line:
            fields.create_line(y, 2, y, 462, fill='grey')
        for x in pos_line:
            fields.create_line(2, x, 462, x, fill='grey')
        fields.create_line(156, 2, 156, 462, width=2)
        fields.create_line(310, 2, 310, 462, width=2)
        fields.create_line(2, 156, 462, 156, width=2)
        fields.create_line(2, 310, 462, 310, width=2)
        fields.pack()
        self.add_fields()

    def add_fields(self):
        """Выводим поля на холсте."""
        self.fields_dict = {}  # Словарь для хранения полей
        pos_xy = [3, 54, 105, 157, 208, 259, 311, 362, 413]
        pos_field = [(x, y) for y in pos_xy for x in pos_xy]
        # pos_field = [(3, 3), (54, 3), (105, 3), ...]
        rows = 1  # начальные значения для строк
        cols = 1  # начальные значения для столбцов
        # Заполняем 81 поле, предварительно определив нужные параметры
        for i in range(1, 82):
            f_num = i
            if cols > 9:
                rows += 1
                cols = 1
            f_row = rows
            f_col = cols
            cols += 1
            # Ищем группу по нужной диапазону строк и столбцов
            if f_row in [1, 2, 3] and f_col in [1, 2, 3]:
                f_group = 1
            if f_row in [1, 2, 3] and f_col in [4, 5, 6]:
                f_group = 2
            if f_row in [1, 2, 3] and f_col in [7, 8, 9]:
                f_group = 3
            if f_row in [4, 5, 6] and f_col in [1, 2, 3]:
                f_group = 4
            if f_row in [4, 5, 6] and f_col in [4, 5, 6]:
                f_group = 5
            if f_row in [4, 5, 6] and f_col in [7, 8, 9]:
                f_group = 6
            if f_row in [7, 8, 9] and f_col in [1, 2, 3]:
                f_group = 7
            if f_row in [7, 8, 9] and f_col in [4, 5, 6]:
                f_group = 8
            if f_row in [7, 8, 9] and f_col in [7, 8, 9]:
                f_group = 9
            # Выводим нужное поле
            self.fields_dict[i] = FieldEntry(self.frame_fields, pos_field[i - 1], f_num, f_row, f_col, f_group)

    def add_region_start(self):
        """Выводим блок - кнопка старт - программы."""
        self.frame_start = tk.Frame(self.root, width=480, height=60, bg="white")
        self.frame_start.pack()
        self.btn_start = tk.Button(self.frame_start, text="Solve", command=self.start_game)
        self.btn_start.place(x=200, y=15)
        self.btn_start["state"] = "disabled"

    def add_region_info(self):
        """Выводим блок - инфа - программы."""
        self.frame_info = tk.Frame(self.root, width=480, height=60)
        self.frame_info.pack()
        self.msg_info = tk.Label(self.frame_info, bg="white", bd=0)
        self.msg_info.pack()
        self.msg_info.configure(text="Fill in five or more fields to get started.")

    def selected_fields(self):
        """Проверяем кол-во заполненных полей."""
        sum_selected = 0
        # Перебираем все поля
        for x in self.fields_dict.values():
            if x.field_get in range(1, 10):
                sum_selected += 1
        # Если их 5 или больше, тогда вкл кнопку Старт
        if sum_selected >= 5:
            self.btn_start["state"] = "active"
            self.msg_info.configure(text="You have filled out {0} fields.".format(sum_selected))
        else:
            self.btn_start["state"] = "disabled"
            self.msg_info.configure(text="You have filled out {0} fields, you need at least five.".format(sum_selected))

    def start_game(self):
        """Запуск программы по кнопке Старт."""
        self.btn_start["state"] = "disabled"
        # # Перебираем все поля
        # for x in self.fields_dict.values():
        #     x.field_insert()


def game_info():
    """Показываем информацию об игре."""
    output = "\nAbout game.\n"
    mb.showinfo(title="About", message=output)


def game_reset():
    """Сброс игры."""
    answer = mb.askyesno(title="Reset", message="Reset the game?")
    if answer is True:
        App.app_reset(sudoku)


def game_exit():
    """Корректное закрытие окна программы."""
    answer = mb.askyesno(title="Exit", message="Close the program?")
    if answer is True:
        root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    sudoku = App(root)
    root.mainloop()
