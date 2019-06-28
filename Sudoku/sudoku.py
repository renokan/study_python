"""Sudoku / Решаем задачи судоку.

Уточнение:
    1. testing() - это декоратор для тестирования
    2. import copy нужен для глубокого копирования некоторых словарей

Особенности реализации:
    1. В меню добавлена возможность (Example) сгенерировать набор значений
    2. Проверка на минимальное кол-во введенных значений
    3. ...
"""
import tkinter as tk
from tkinter import messagebox as mb
import random


def testing(search_numbers):
    """Выводим получившиеся результаты, для тестирования."""
    def wrapper(self):
        search_numbers(self)
        # Считаем кол-во найденных полей
        check = sum([len(x) for x in self.search_groups.values()])
        # Если не все поля найдены, тогда принтим инфу для анализа
        if check != 81:
            print("\nFound {} fields.".format(check))

            print("\nself.fields_rows:")
            for (key, value) in sorted(self.fields_rows.items(), key=lambda x: len(x[1])):
                print("row: {0} -> {1}".format(key, value))

            print("\nself.fields_cols:")
            for (key, value) in sorted(self.fields_cols.items(), key=lambda x: len(x[1])):
                print("col: {0} -> {1}".format(key, value))

            print("\nself.fields_groups:")
            for (key, value) in sorted(self.fields_groups.items(), key=lambda x: len(x[1])):
                print("group: {0} -> {1}".format(key, value))

            print("\nList:  num -> row - col - group -> field_search")
            for i in range(1, 82):
                if len(self.fields_dict[i].field_search) > 0:
                    f_row = self.fields_dict[i].num_row
                    f_col = self.fields_dict[i].num_col
                    f_group = self.fields_dict[i].num_group
                    f_search = self.fields_dict[i].field_search
                    print("field: {0} -> {1} - {2} - {3} -> {4}".format(i, f_row, f_col, f_group, f_search))

    return wrapper


class FieldEntry:
    """Это класс полей (тип Entry) для ввода цифр."""

    def __init__(self, reg_field, f_xy, f_num, f_row, f_col, f_group):
        """Что делаем при инициализации класса."""
        self.num_field = f_num
        self.num_row = f_row
        self.num_col = f_col
        self.num_group = f_group
        self.field_get = ''
        self.field_search = None
        self.field_insert = ''
        self.field = tk.Entry(reg_field, bd=1, bg='white', justify="center")
        self.field.bind('<FocusOut>', self.check_input)
        self.field.place(x=f_xy[0], y=f_xy[1], width=48, height=48)

    def insert_num(self, num_insert=None):
        """Записываем число в нужное поле."""
        self.field.delete(0, "end")
        if num_insert:
            self.field.insert(0, num_insert)

    def check_input(self, event):
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
        self.add_canvas()
        self.add_region_start()
        self.add_region_info()

    def app_reset(self):
        """Обнуляем окно программы программы."""
        self.frame_fields.destroy()
        self.add_canvas()
        self.frame_start.destroy()
        self.add_region_start()
        self.frame_info.destroy()
        self.add_region_info()

    def app_create(self):
        """Конфигурируем окно программы."""
        width = 480
        height = 600
        # Название и фон
        self.root.title('Sudoku')
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
        top_menu.add_command(label="Example", command=self.input_example)
        top_menu.add_command(label="Exit", command=game_exit)

    def add_canvas(self):
        """Выводим блок - холст - программы."""
        self.frame_fields = tk.Frame(self.root, width=480, height=480, bg="white", bd=8)
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
        self.msg_info.configure(text="Fill in five or more fields to get started.", fg='navy')

    def selected_fields(self):
        """Проверяем заполненные поля."""
        sum_selected = 0
        self.dict_selected = {}
        # Перебираем все поля
        for key, field in self.fields_dict.items():
            if field.field_get in range(1, 10):
                self.dict_selected[key] = field.field_get
                sum_selected += 1
        # Если их 5 или больше, тогда вкл кнопку Старт
        if sum_selected >= 5:
            self.btn_start["state"] = "active"
            self.msg_info.configure(text="You have filled out {0} fields.".format(sum_selected), fg='black')
        else:
            self.btn_start["state"] = "disabled"
            self.msg_info.configure(text="You have filled out {0} fields, you need at least five.".format(sum_selected), fg='black')

    def check_selected(self):
        """Проверяем заполненные поля."""
        # Формируем словари полей для строк, столбцов и групп. Для поиска надо.
        self.fields_rows = {k: set([i for i in range(1, 82) if self.fields_dict[i].num_row == k]) for k in range(1, 10)}
        self.fields_cols = {k: set([i for i in range(1, 82) if self.fields_dict[i].num_col == k]) for k in range(1, 10)}
        self.fields_groups = {k: set([i for i in range(1, 82) if self.fields_dict[i].num_group == k]) for k in range(1, 10)}
        # Формируем словари ...
        self.selected_rows = {k: [] for k in range(1, 10)}
        self.selected_cols = {k: [] for k in range(1, 10)}
        self.selected_groups = {k: [] for k in range(1, 10)}
        # Перебираем заполненные поля
        for key, field in self.dict_selected.items():
            num_row = self.fields_dict[key].num_row
            num_col = self.fields_dict[key].num_col
            num_group = self.fields_dict[key].num_group
            # Формируем (добавляем значения) словарь
            self.selected_rows[num_row].append(field)
            self.selected_cols[num_col].append(field)
            self.selected_groups[num_group].append(field)
            # Формируем (удаляем номера полей) словарь
            self.fields_rows[num_row].discard(key)
            self.fields_cols[num_col].discard(key)
            self.fields_groups[num_group].discard(key)
        # Проверяем чтобы в строке не было повторений
        for key, value in self.selected_rows.items():
            for x in range(1, 10):
                if value.count(x) > 1:
                    return "You have entered several '{}' values ​​in the row.".format(x)
        # Проверяем чтобы в столбце не было повторений
        for key, value in self.selected_cols.items():
            for x in range(1, 10):
                if value.count(x) > 1:
                    return "You have entered several '{}' values ​​in the column.".format(x)
        # Проверяем чтобы в группе не было повторений
        for key, value in self.selected_groups.items():
            for x in range(1, 10):
                if value.count(x) > 1:
                    return "You have entered several '{}' values ​​in the group.".format(x)

    def upd_dicts(self, f_num, f_value):
        """Обновляем словари, исходные данные берём из найденного значения."""
        row = self.fields_dict[f_num].num_row
        col = self.fields_dict[f_num].num_col
        group = self.fields_dict[f_num].num_group

        # Если значения нет в словаре то добавляем его
        self.search_rows[row].add(f_value)
        self.search_cols[col].add(f_value)
        self.search_groups[group].add(f_value)

        # Если это поле есть в словаре то удаляем его
        self.fields_rows[row].discard(f_num)
        self.fields_cols[col].discard(f_num)
        self.fields_groups[group].discard(f_num)

    @testing
    def search_numbers(self):
        """Ищем номера."""
        self.search_rows = {key: set(value) for key, value in self.selected_rows.items()}
        self.search_cols = {key: set(value) for key, value in self.selected_cols.items()}
        self.search_groups = {key: set(value) for key, value in self.selected_groups.items()}
        # selected_rows = {1: [5, 9, 3, 1, 7, 8], 2: [4, 2, 9, 1, 3], 3: [3, 4, 5, 9, 2], 4: [5], 5:
        # selected_cols =  {1: [3, 8, 5], 2: [5, 3, 2, 4], 3: [9, 4, 8, 7, 2], 4: [3, 2, 9, 8]
        # selected_groups = {1: [5, 9, 4, 3], 2: [3, 1, 7, 2, 9, 4], 3: [8, 1, 3, 5, 9, 2], 4: [2, 8, 3]

        # Перебираем все поля и заполняем исходные данные
        for i in range(1, 82):
            self.fields_dict[i].field_search = set([x for x in range(1, 10)])
            if self.fields_dict[i].field_get != '':
                self.fields_dict[i].field_search.clear()
                self.fields_dict[i].field_insert = 0

        step = 0
        while True:
            # Проверяем кол-во полей во всех группах перед поиском
            check_start = sum([len(x) for x in self.search_groups.values()])
            # 1 этап: обходим отсортированные словари fields_row(col,group)s
            for (key, value) in sorted(self.fields_rows.items(), key=lambda x: len(x[1])):
                # 1: [1, 7, 8], 2: [10, 11, 15, 16], 6: [47, 48, 50, 51, 52]...
                if len(value) > 0:
                    for i in value.copy():
                        if len(self.fields_dict[i].field_search) > 0:
                            x = self.fields_dict[i].num_row
                            self.fields_dict[i].field_search = self.fields_dict[i].field_search - self.search_rows[x]
                            if len(self.fields_dict[i].field_search) == 1:
                                result = self.fields_dict[i].field_search.pop()
                                self.fields_dict[i].field_insert = result
                                self.upd_dicts(i, result)
                else:
                    self.fields_rows.pop(key)
            for (key, value) in sorted(self.fields_cols.items(), key=lambda x: len(x[1])):
                # 9: [63, 72], 3: [21, 30, 48, 57], 2: [11, 29, 47, 56, 65]...
                if len(value) > 0:
                    for i in value.copy():
                        if len(self.fields_dict[i].field_search) > 0:
                            x = self.fields_dict[i].num_col
                            self.fields_dict[i].field_search = self.fields_dict[i].field_search - self.search_cols[x]
                            if len(self.fields_dict[i].field_search) == 1:
                                result = self.fields_dict[i].field_search.pop()
                                self.fields_dict[i].field_insert = result
                                self.upd_dicts(i, result)
                else:
                    self.fields_cols.pop(key)
            for (key, value) in sorted(self.fields_groups.items(), key=lambda x: len(x[1])):
                # 3: [16], 2: [15, 22, 24], 1: [1, 10, 11, 19, 21]...
                if len(value) > 0:
                    for i in value.copy():
                        if len(self.fields_dict[i].field_search) > 0:
                            x = self.fields_dict[i].num_group
                            self.fields_dict[i].field_search = self.fields_dict[i].field_search - self.search_groups[x]
                            if len(self.fields_dict[i].field_search) == 1:
                                result = self.fields_dict[i].field_search.pop()
                                self.fields_dict[i].field_insert = result
                                self.upd_dicts(i, result)
                else:
                    self.fields_groups.pop(key)

            # 2 этап: в отсортированном словаре fields_groups берём значения
            # полей для каждой группы, берём все field_search и ищем уникальное
            # значение, далее по нему ищем поле где оно было и его обновляем.
            for (key, value) in sorted(self.fields_groups.items(), key=lambda x: len(x[1])):
                # 2: [15, 24], 9: [62, 79, 80], 4: [28, 29, 37, 47], 6: [34, 35, 43, 52]...
                if len(value) > 0:
                    all = []
                    for i in value:
                        if len(self.fields_dict[i].field_search) > 0:
                            for x in self.fields_dict[i].field_search:
                                all.append(x)
                    all = [i for i in all if i not in self.search_groups[key]]
                    for s in all:
                        if all.count(s) == 1:
                            for i in value.copy():
                                if s in self.fields_dict[i].field_search:
                                    self.fields_dict[i].field_search.clear()
                                    self.fields_dict[i].field_insert = s
                                    self.upd_dicts(i, s)
                else:
                    self.fields_groups.pop(key)

            # Проверяем кол-во полей во всех группах после поиска
            check_end = sum([len(x) for x in self.search_groups.values()])

            if check_end == 81:
                # Если нашли все поля, тогда
                break
            elif check_end == check_start:
                # Если после поиска ничего не изменилось, тогда
                step += 1  # делаем ещё несколько попыток
                # Если было 3 безуспешные попытки, тогда
                if step == 3:
                    return "Unfortunately, no solution was found!"

    def start_game(self):
        """Запуск программы по кнопке Старт."""
        self.btn_start["state"] = "disabled"
        check = self.check_selected()
        if check:
            self.msg_info.configure(text=check, fg='red')
        else:
            check = self.search_numbers()
            if check:
                self.msg_info.configure(text=check, fg='red')
            else:
                self.msg_info.configure(text="Congratulations, the solution is found!", fg='green')
            # В не зависимости сколько полей нашли, нужно показать их пользователю
            self.insert_result()

    def input_example(self):
        """Вводим значения по умолчанию, для тестирования."""
        ex_1 = {2: 5, 3: 9, 4: 3, 5: 1, 6: 7, 9: 8, 12: 4, 13: 2, 14: 9, 17: 1, 18: 3, 20: 3, 23: 4, 25: 5, 26: 9, 27: 2, 36: 5, 38: 2, 39: 8, 40: 9, 44: 7, 45: 6, 46: 3, 49: 8, 53: 2, 54: 4, 61: 4, 64: 8, 66: 7, 70: 2, 71: 6, 73: 5, 74: 4, 75: 2, 81: 1}
        ex_2 = {1: 5, 7: 7, 8: 9, 10: 1, 13: 4, 16: 5, 17: 8, 18: 2, 22: 5, 30: 1, 31: 2, 32: 9, 36: 6, 37: 8, 38: 3, 42: 7, 46: 4, 47: 9, 50: 5, 51: 8, 52: 3, 54: 7, 55: 9, 56: 8, 63: 3, 65: 2, 71: 1, 76: 3}
        ex_3 = {1: 8, 8: 3, 10: 9, 12: 5, 14: 3, 18: 8, 19: 6, 20: 4, 28: 5, 31: 8, 32: 2, 36: 6, 39: 8, 42: 5, 47: 2, 50: 7, 51: 9, 53: 5, 59: 6, 64: 1, 69: 3, 70: 5, 72: 2, 75: 6, 76: 2, 77: 1, 78: 4, 79: 7}
        ex_4 = {3: 2, 5: 9, 8: 5, 10: 3, 11: 7, 13: 6, 14: 4, 16: 1, 18: 8, 20: 9, 21: 1, 25: 4, 27: 6, 40: 9, 41: 3, 42: 1, 47: 4, 51: 6, 52: 9, 54: 7, 55: 9, 60: 5, 67: 4, 70: 5, 73: 5, 77: 1, 78: 3, 80: 8}
        examles = {1: ex_1, 2: ex_2, 3: ex_3, 4: ex_4}

        # Чистим все поля от того, что было
        for i in range(1, 82):
            self.fields_dict[i].insert_num()
            self.fields_dict[i].field_get = ''
            self.fields_dict[i].field_insert = ''
            self.fields_dict[i].field.configure(bg='white')


        # Заполняем нужные поля значения из словаря (выбираем random)
        for key, value in examles[random.randint(1, 4)].items():
            if value != '':
                self.fields_dict[key].insert_num(value)
                self.fields_dict[key].field_get = value
                self.fields_dict[key].field.configure(bg='lightgrey')

        # Проверяем заполненные поля
        self.selected_fields()

    def insert_result(self):
        """Вводим найденные значения."""
        for i in range(1, 82):
            if self.fields_dict[i].field_insert in range(1, 10):
                self.fields_dict[i].insert_num(self.fields_dict[i].field_insert)


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
