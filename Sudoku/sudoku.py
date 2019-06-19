"""Game "Sudoku"."""
import tkinter as tk
from tkinter import messagebox as mb
from math import sqrt


class FieldEntry:
    """Это класс полей (тип Entry) для ввода цифр."""

    # Глобальные переменные: ряд, столбец, группы полей, размеры грани и полей
    rows = 1
    cols = 1
    groups = {}
    side = 9
    size = 48

    def __init__(self, reg_field, num_field, pos_xy):
        """Что делаем при инициализации класса."""
        self.num_field = num_field
        self.num_row, self.num_col = self.row_col()

        # Если словарь с группами пустой, тогда нужно его создать
        if len(FieldEntry.groups) == 0:
            self.group_fields()
        # Перебираем словарь с группами и ищем соотвествие ряда и столбца
        for key, value in sorted(FieldEntry.groups.items()):
            # groups = {1: ((1, 2, 3), (1, 2, 3)), 2: ((1, 2, 3), (4, 5, 6)),
            #           3: ((1, 2, 3), (7, 8, 9)), 4: ((4, 5, 6), (1, 2, 3)),
            #           ...
            #           }
            if self.num_row in value[0]:
                if self.num_col in value[1]:
                    self.num_group = key

        self.field_get = ''
        self.field_search = [x for x in range(1, 10)]

        self.field = tk.Entry(reg_field, bd=1, bg='white', justify="center")
        self.field.bind('<FocusOut>', self.check_get)
        self.field.place(x=pos_xy[0], y=pos_xy[1], width=self.size, height=self.size)

        # self.field.insert(0, self.num_field)
        # self.field.insert(0, self.num_group)

    def row_col(self):
        """Проверяем текущий ряд и столбец, возвращаем новые данные."""
        # Сравниваем текущий столбец и длину грани нашей матрицы, если
        # выходим за грань - тогда переходим на новый ряд и первый столбец
        if FieldEntry.cols > self.side:
            FieldEntry.rows += 1
            FieldEntry.cols = 1
        result = (FieldEntry.rows, FieldEntry.cols)
        FieldEntry.cols += 1
        return result

    def group_fields(self):
        """Словарь, где ключ это номер группы, а значение (ряды и столбцы)."""
        list_row_col = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        temp = [(l_row, l_col) for l_row in list_row_col for l_col in list_row_col]
        FieldEntry.groups = {k + 1: temp[k] for k in range(len(temp))}
        # groups = {1: ((1, 2, 3), (1, 2, 3)), 2: ((1, 2, 3), (4, 5, 6)),
        #           3: ((1, 2, 3), (7, 8, 9)), 4: ((4, 5, 6), (1, 2, 3)),
        #           ...
        #           }

    def field_insert(self, num_insert):
        """Записываем число в нужное поле."""
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
        pos_xy = [3, 54, 105, 157, 208, 259, 311, 362, 413]
        pos_field = [(x, y) for y in pos_xy for x in pos_xy]
        # pos_field = [(3, 3), (54, 3), (105, 3), ...]
        # len(pos_field) - 81 / 9*9
        FieldEntry.side = int(sqrt(len(pos_field)))
        FieldEntry.size = 48
        self.fields_dict = {}
        for i in range(len(pos_field)):
            self.fields_dict[i + 1] = FieldEntry(self.frame_fields, i + 1, pos_field[i])

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
