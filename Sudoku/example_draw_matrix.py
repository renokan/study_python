"""
Example draw a matrix / Рисуем матрицу произвольного размера.

Пользователь выбирает какую матрицу он хочет - 4x4, 9x9, 16x16, 25x25.
Также можно выбирать размер поля в пикселях: 30, 40, 50 или 60 px.
Можно выбирать, заполнять ли матрицу полями, если - чем их заполнить.
"""

import tkinter as tk
from tkinter import messagebox as mb
from math import sqrt


class FieldEntry:
    """Это класс полей (тип Entry) для ввода цифр."""

    def __init__(self, f_region, f_xy, f_size, f_insert=None):
        """Что делаем при инициализации класса."""
        size = f_size - 2  # bd=1 - слева и справа
        self.field = tk.Entry(f_region, bd=1, bg='white', justify="center")
        self.field.place(x=f_xy[0], y=f_xy[1], width=size, height=size)

        if f_insert:
            self.field.insert(0, f_insert)


class App:
    """Это класс с данными программы, если нужно будет их обнулить."""

    def __init__(self, root):
        """Что делаем при инициализации класса."""
        self.root = root
        self.app_create()
        self.add_region_start()
        self.add_canvas()

    def app_reset(self):
        """Обнуляем окно программы программы."""
        self.frame_start.destroy()
        self.add_region_start()
        self.frame_fields.destroy()
        self.add_canvas()

    def app_create(self):
        """Конфигурируем окно программы."""
        self.root.title('Example draw a matrix')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        # Меню
        top_menu = tk.Menu(self.root)
        self.root.config(menu=top_menu)
        top_menu.add_command(label="About", command=program_info)
        top_menu.add_command(label="Reset", command=program_reset)
        top_menu.add_command(label="Exit", command=program_exit)

    def add_region_start(self):
        """Выводим блок - кнопка старт - программы."""
        self.frame_start = tk.Frame(self.root, bg="white")
        self.frame_start.pack()

        self.frame_config = tk.Frame(self.frame_start, bg="white", bd=10)
        self.frame_config.pack()

        # ** Блок с данными
        # 1. Размер матрицы
        label_matrix_side = tk.Label(self.frame_config, text='Matrix size:', bg='white')
        self.matrix_side = tk.IntVar()
        self.matrix_side.set(9)
        select_matrix_4 = tk.Radiobutton(self.frame_config, text='4 x 4', variable=self.matrix_side, value=4, command=self.draw_matrix)
        select_matrix_9 = tk.Radiobutton(self.frame_config, text='9 x 9', variable=self.matrix_side, value=9, command=self.draw_matrix)
        select_matrix_16 = tk.Radiobutton(self.frame_config, text='16 x 16', variable=self.matrix_side, value=16, command=self.draw_matrix)
        select_matrix_25 = tk.Radiobutton(self.frame_config, text='25 x 25', variable=self.matrix_side, value=25, command=self.draw_matrix)
        select_matrix_4.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_matrix_9.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_matrix_16.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_matrix_25.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        label_matrix_side.grid(row=0, column=0, sticky="E")
        select_matrix_4.grid(row=0, column=1, sticky="W")
        select_matrix_9.grid(row=0, column=2, sticky="W")
        select_matrix_16.grid(row=0, column=3, sticky="W")
        select_matrix_25.grid(row=0, column=4, sticky="W")
        # 2. Размер полей
        label_matrix_size = tk.Label(self.frame_config, text='Field size:', bg='white')
        self.matrix_size = tk.IntVar()
        self.matrix_size.set(50)
        select_size_30 = tk.Radiobutton(self.frame_config, text='30 px', variable=self.matrix_size, value=30, command=self.draw_matrix)
        select_size_40 = tk.Radiobutton(self.frame_config, text='40 px', variable=self.matrix_size, value=40, command=self.draw_matrix)
        select_size_50 = tk.Radiobutton(self.frame_config, text='50 px', variable=self.matrix_size, value=50, command=self.draw_matrix)
        select_size_60 = tk.Radiobutton(self.frame_config, text='60 px', variable=self.matrix_size, value=60, command=self.draw_matrix)
        select_size_30.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_size_40.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_size_50.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_size_60.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        label_matrix_size.grid(row=1, column=0, sticky="E")
        select_size_30.grid(row=1, column=1, sticky="W")
        select_size_40.grid(row=1, column=2, sticky="W")
        select_size_50.grid(row=1, column=3, sticky="W")
        select_size_60.grid(row=1, column=4, sticky="W")
        # 3. В поле пишем
        label_matrix_info = tk.Label(self.frame_config, text='Fill in the field:', bg='white')
        self.matrix_info = tk.IntVar()
        self.matrix_info.set(0)
        select_info_none = tk.Radiobutton(self.frame_config, text='none', variable=self.matrix_info, value=0, command=self.draw_matrix)
        select_info_empty = tk.Radiobutton(self.frame_config, text='empty', variable=self.matrix_info, value=1, command=self.draw_matrix)
        select_info_num = tk.Radiobutton(self.frame_config, text='number', variable=self.matrix_info, value=2, command=self.draw_matrix)
        select_info_group = tk.Radiobutton(self.frame_config, text='group', variable=self.matrix_info, value=3, command=self.draw_matrix)
        select_info_none.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_info_empty.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_info_num.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        select_info_group.config(bg='white', bd=2, highlightbackground='white', activebackground='white')
        label_matrix_info.grid(row=2, column=0, sticky="E")
        select_info_none.grid(row=2, column=1, sticky="W")
        select_info_empty.grid(row=2, column=2, sticky="W")
        select_info_num.grid(row=2, column=3, sticky="W")
        select_info_group.grid(row=2, column=4, sticky="W")

    def add_canvas(self):
        """Выводим блок - холст - программы."""
        self.frame_fields = tk.Frame(self.root, bg="white", bd=5)
        self.frame_fields.pack()

        self.m_info = self.matrix_info.get()  # none / empty / number / group
        self.f_size = self.matrix_size.get()  # 30 / 40 / 50 / 60 ...
        self.m_size = self.matrix_side.get()  # 4 / 9 / 16 / 25 ...
        self.m_amt_side = int(sqrt(self.m_size))  # 2 / 3 / 4 / 5 ...
        self.m_amt_line = self.m_amt_side - 1  # 1 / 2 / 3 / 4 ...
        self.bd_1 = 1  # Ширина тонкой линии в px
        self.bd_2 = 2  # Ширина толстой линии в px
        m_side = ((self.m_size * self.f_size) + ((self.m_amt_line + self.bd_2) * 2) + (self.m_amt_line * self.m_amt_side * self.bd_1))
        fields = tk.Canvas(self.frame_fields, width=m_side, height=m_side, bg="gray70", bd=0, highlightthickness=0)
        # Рисуем прямоугольник
        fields.create_rectangle(self.bd_1, self.bd_1, m_side - self.bd_1, m_side - self.bd_1, width=self.bd_2)
        # Рисуем тонкие линии разметки
        xy_line = []
        xy_bd_1 = self.bd_2
        for i in range(self.m_amt_side):
            for z in range(1, self.m_amt_side):
                xy_bd_1 += self.f_size + self.bd_1
                xy_line.append(xy_bd_1)
                # xy_line = [53, 104, 207, 258, 361, 412...
            xy_bd_1 += self.f_size + self.bd_2
        # -> вертикальные
        for x in xy_line:
            fields.create_line(x, self.bd_2, x, m_side - self.bd_2, fill='grey')
        # -> горизонтальные
        for y in xy_line:
            fields.create_line(self.bd_2, y, m_side - self.bd_2, y, fill='grey')
        # Рисуем толстые линии разметки
        for i in range(1, self.m_amt_side):
            i_xy = self.bd_2 + (i * 1) + (self.m_amt_side * self.f_size * i) + (self.m_amt_line * self.bd_1 * i) + (i * 1)
            fields.create_line(i_xy, self.bd_2, i_xy, m_side - self.bd_2, width=self.bd_2)
            fields.create_line(self.bd_2, i_xy, m_side - self.bd_2, i_xy, width=self.bd_2)
        # Всё, разметка готова
        fields.pack()
        # Если нужно показать поля (выбран вариант 1, 2 или 3)
        if self.m_info != 0:
            self.add_fields()

    def add_fields(self):
        """Выводим поля на холсте."""
        xy_field = self.bd_2 + 1  # первое поле
        pos_xy = [xy_field]
        for i in range(self.m_amt_side):
            for z in range(self.m_amt_line):
                xy_field += self.f_size + self.bd_1
                pos_xy.append(xy_field)
            xy_field += self.f_size + self.bd_2
            if len(pos_xy) < self.m_size:
                pos_xy.append(xy_field)
        # pos_xy = [3, 54, 105, 157, 208, 259, 311, 362, 413]
        pos_field = [(x, y) for y in pos_xy for x in pos_xy]
        # pos_field = [(3, 3), (54, 3), (105, 3), (157, 3), (208, 3), (259, 3),

        groups = self.group_fields()
        rows = 1  # начальные значения для строк
        cols = 1  # начальные значения для столбцов

        for i in range(len(pos_field)):

            f_num = i + 1
            if cols > self.m_size:
                rows += 1
                cols = 1
            f_row = rows
            f_col = cols
            cols += 1

            for key, value in sorted(groups.items()):
                if f_row in value[0]:
                    if f_col in value[1]:
                        f_group = key

            if self.m_info == 2:
                f_insert = f_num
            elif self.m_info == 3:
                f_insert = f_group
            else:
                f_insert = None

            FieldEntry(self.frame_fields, pos_field[i], self.f_size, f_insert)

    def group_fields(self):
        """Словарь, где ключ это номер группы, а значение (строки и столбцы)."""
        list_num = [x for x in range(1, self.m_size + 1)]  # [1, 2, 3, 4, ...]
        x = 0  # начальное нулевое значение чтобы делать срез из list_num
        list_row_col = []

        for i in range(self.m_amt_side):
            list_row_col.extend([list_num[x:x + self.m_amt_side]])
            x += self.m_amt_side
        # list_row_col = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

        col_side = [(l_row, l_col) for l_row in list_row_col for l_col in list_row_col]
        # [([1, 2, 3], [1, 2, 3]), ([1, 2, 3], [4, 5, 6]), ([1, 2, 3], [7, 8, 9]),
        #  ([4, 5, 6], [1, 2, 3]), ([4, 5, 6], [4, 5, 6]), ([4, 5, 6], [7, 8, 9]),

        return {k + 1: col_side[k] for k in range(len(col_side))}
        # {1: ((1, 2, 3), (1, 2, 3)), 2: ((1, 2, 3), (4, 5, 6)),
        #  3: ((1, 2, 3), (7, 8, 9)), 4: ((4, 5, 6), (1, 2, 3)),
        #  ...
        #  }

    def draw_matrix(self):
        """Запуск программы по кнопке Старт."""
        self.frame_fields.destroy()
        self.add_canvas()
        window_center(root)


def program_info():
    """Показываем информацию о программе."""
    output = "\nAutomatically draw a matrix.\n"
    output += "\nYou can choose the size of the matrix, as well as the size of the fields and how to fill them.\n"
    mb.showinfo(title="About", message=output)


def program_reset():
    """Сброс игры."""
    answer = mb.askyesno(title="Reset", message="Reset the program?")
    if answer is True:
        App.app_reset(matrix)


def program_exit():
    """Корректное закрытие окна программы."""
    answer = mb.askyesno(title="Exit", message="Close the program?")
    if answer is True:
        root.destroy()


def window_center(toplevel):
    """Окно по центру."""
    toplevel.update_idletasks()
    width = toplevel.winfo_reqwidth()
    height = toplevel.winfo_reqheight()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    if width > screen_width:
        x = 0
    else:
        x = (screen_width / 2) - (width / 2)
    if height > screen_height:
        y = 0
    else:
        y = (screen_height / 2) - (height / 1.4)
    toplevel.geometry('+%d+%d' % (x, y))


if __name__ == '__main__':
    root = tk.Tk()
    matrix = App(root)
    window_center(root)
    root.mainloop()
