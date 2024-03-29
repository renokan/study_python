"""
EditorFiles / Редактор файлов.

Программа показывает текущую директорию, можно поменять.

Для работы с файлом, можно:
    А. Создать новый
    Б. Загрузить существующий

После того как будет выбран файл, определяем его:
    1. размер
    2. время

Также становятся доступны кнопки Сохранить и Удалить текущий файл.

При каждом действии, связанным с модификацией файла, спрашиваем у пользователя.
"""

import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import os
import time


class App:
    """Это класс с данными программы."""

    def __init__(self, root):
        """Что делаем при инициализации класса."""
        self.root = root
        self.sizes = ((60, 12), (80, 14), (100, 16), (120, 18), (140, 20), (160, 22), (180, 24))
        self.app_size = self.sizes[1]
        self.app_create()
        self.reg_directory()
        self.reg_activate()
        self.reg_data()
        self.reg_info()
        self.reg_action()

    def size_increase(self):
        """Увеличиваем окно программы."""
        if self.app_size != self.sizes[-1]:
            x = self.sizes.index(self.app_size) + 1
            self.app_size = self.sizes[x]
            self.file_data.config(width=self.app_size[0], height=self.app_size[1])
            window_center(root)

    def size_reduce(self):
        """Уменьшаем окно программы."""
        if self.app_size != self.sizes[0]:
            x = self.sizes.index(self.app_size) - 1
            self.app_size = self.sizes[x]
            self.file_data.config(width=self.app_size[0], height=self.app_size[1])
            window_center(root)

    def app_create(self):
        """Конфигурируем окно программы."""
        # Название и фон
        self.root.title('Editor files')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        # Меню
        top_menu = tk.Menu(self.root)
        self.root.config(menu=top_menu)
        top_menu.add_command(label="Size+", command=self.size_increase)
        top_menu.add_command(label="Size-", command=self.size_reduce)
        top_menu.add_command(label="About", command=app_info)
        top_menu.add_command(label="Exit", command=app_exit)

    def reg_directory(self):
        """Выводим блок - текущая директория."""
        self.reg_dir = tk.Frame(self.root, height=70, bg="white")
        self.reg_dir.pack(fill="x")

        self.dir_label = tk.Label(self.reg_dir, text="Current directory:", bg="white", bd=0)
        self.dir_btn = tk.Button(self.reg_dir, text="Change", command=self.change_dir)
        self.dir_info = tk.Label(self.reg_dir, text=os.getcwd(), bg="white", bd=0)

        self.dir_label.place(x=10, y=13)
        self.dir_btn.place(x=135, y=6)
        self.dir_info.place(x=10, y=43)

    def reg_activate(self):
        """Выводим блок - активация файла."""
        reg_activate = tk.Frame(self.root, height=70, bg="white")
        reg_activate.pack(fill="x")

        file_label = tk.Label(reg_activate, text="File name:", bg="white", bd=0)
        self.file_name = tk.Entry(reg_activate, bd=1, bg='white', width=15)
        file_btn = tk.Button(reg_activate, text="Create", command=self.create_file)

        txt_load = tk.Label(reg_activate, text="or load file", bg="white", bd=0)
        select_btn = tk.Button(reg_activate, text="Select file", command=self.load_file)

        file_label.place(x=10, y=10)
        self.file_name.place(x=10, y=37)
        file_btn.place(x=150, y=33)
        txt_load.place(x=225, y=40)
        select_btn.place(x=300, y=33)

    def reg_data(self):
        """Выводим блок - содержимое файла - программы."""
        self.reg_file = tk.Frame(self.root, bg="white", bd=5)
        self.reg_file.pack(fill="x")
        self.file_data = tk.Text(self.reg_file, width=self.app_size[0], height=self.app_size[1], bg="gray80", fg='black', wrap="word")
        self.file_data.pack(side="left", fill="x")
        scroll = tk.Scrollbar(self.reg_file, command=self.file_data.yview)
        scroll.pack(side="left", fill="both")
        self.file_data.config(yscrollcommand=scroll.set)

    def reg_info(self):
        """Выводим блок - информация о файле."""
        reg_info = tk.Frame(self.root, height=40, bg="white")
        reg_info.pack(fill="x")

        time_label = tk.Label(reg_info, text="Time:", bg="white", bd=0)
        self.time_info = tk.Label(reg_info, bg="white", bd=0)
        size_label = tk.Label(reg_info, text="Size:", bg="white", bd=0)
        self.size_info = tk.Label(reg_info, bg="white", bd=0)

        time_label.place(x=10, y=10)
        self.time_info.place(x=50, y=10)
        size_label.place(x=200, y=10)
        self.size_info.place(x=235, y=10)

    def reg_action(self):
        """Выводим блок - Сохранить и Удалить."""
        reg_action = tk.Frame(self.root, height=40, bg="white", bd=5)
        reg_action.pack()

        self.save_btn = tk.Button(reg_action, text="Save file", command=self.save_file)
        self.del_btn = tk.Button(reg_action, text="Delete file", command=self.del_file)
        self.save_btn["state"] = "disabled"
        self.del_btn["state"] = "disabled"

        self.save_btn.grid(row=0, column=0, pady=5, padx=5, sticky="E")
        self.del_btn.grid(row=0, column=1, pady=5, padx=5, sticky="W")

    def change_dir(self):
        """Меняем текущую директорию."""
        new_dir = fd.askdirectory()
        if new_dir:
            os.chdir(new_dir)
            if os.sep != '/':
                # Через askdirectory путь получаем с разделителем "/",
                # а в Windows он "\" - поэтому меняем его.
                new_dir = os.path.normpath(new_dir)
            self.dir_info.configure(text=new_dir)

    def create_file(self):
        """Создаем новый файл."""
        name = self.file_name.get()
        if name:
            path_to_file = os.getcwd() + os.sep + name
            try:
                with open(path_to_file, 'x') as f:
                    data = self.file_data.get(1.0, "end")
                    if data:
                        f.write(data)
            except FileExistsError:
                # Уведомление о неудачном действии с файлом
                text = "\nThis file already exists.\n"
                mb.showerror(title="Error", message=text)
            except FileNotFoundError:
                # Уведомление о неудачном действии с файлом
                text = "\nNo such file or directory.\n"
                mb.showerror(title="Error", message=text)
            else:
                # Уведомление об успешном действии с файлом
                text = "\nFile {0} successfully created.\n".format(name)
                mb.showinfo(title="New file", message=text)
                # Обновляем информацию о файле
                self.info_file(path_to_file)
        else:
            # Уведомление о неудачном действии
            text = "\nMissing file name.\n"
            mb.showerror(title="Error", message=text)

    def load_file(self):
        """Загружаем файл."""
        path_to_file = fd.askopenfilename(initialdir=os.getcwd(), title="Choose a file", filetypes=(("TXT files", "*.txt"), ("all files", "*.*")))
        if path_to_file:
            if os.sep != '/':
                # Через askopenfilename путь получаем с разделителем "/",
                # а в Windows он "\" - поэтому меняем его.
                path_to_file = os.path.normpath(path_to_file)
            try:
                with open(path_to_file, encoding='utf-8') as f:
                    temp = f.read()
            except Exception:
                # Уведомление о неудачном действии с файлом
                text = "\nError loading file.\n"
                mb.showerror(title="Error load", message=text)
            else:
                # Записываем данные в поля (tk.Entry)
                self.file_data.delete(1.0, "end")
                self.file_data.insert(1.0, temp)
                self.file_name.delete(0, "end")
                self.file_name.insert(0, os.path.basename(path_to_file))
                # Обновляем информацию о файле
                self.info_file(path_to_file)

    def info_file(self, path_to_file):
        """Собираем информацию о файле."""
        file_time = int(os.path.getmtime(path_to_file))
        file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time))
        file_size = os.path.getsize(path_to_file)
        if file_size < 1024:
            size_num = "B"
        elif file_size >= 1048576:
            # 1024 * 1024
            file_size = file_size / 1024  # KB с усечением
            file_size = round((file_size / 1024), 2)  # MB. Округляем до 2 знаков
            size_num = "MB"
        else:
            file_size = round(file_size / 1024)  # KB
            size_num = "KB"
        file_size = "{0} {1}".format(file_size, size_num)
        # Обновляем информацию - время и размер файла
        self.time_info.config(text=file_time)
        self.size_info.config(text=file_size)
        # Активируем кнопки для работы с файлом
        self.save_btn.config(state="active")
        self.del_btn.config(state="active")
        # Записываем данные по текущему файлу в переменную, для работы с файлом
        self.cur_file_path = path_to_file
        self.cur_file_name = os.path.basename(path_to_file)

    def del_file(self):
        """Удаляем файл."""
        text = "Delete file {0}?".format(self.cur_file_name)
        answer = mb.askyesno(title="Delete", message=text)
        if answer is True:
            os.remove(self.cur_file_path)
            self.cur_file_path = ""
            # Уведомление об успешном действии с файлом
            text = "File {0} has been deleted.".format(self.cur_file_name)
            mb.showinfo(title="Info", message=text)
            # Чистим поля (tk.Entry) от данных
            self.file_name.delete(0, "end")
            self.file_data.delete(1.0, "end")
            self.time_info.config(text="")
            self.size_info.config(text="")
            # Отключаем кнопки
            self.save_btn.config(state="disabled")
            self.del_btn.config(state="disabled")

    def save_file(self):
        """Сохраняем содержимое файла."""
        text = "Save file {0}?".format(self.cur_file_name)
        answer = mb.askyesno(title="Save", message=text)
        if answer is True:
            data = self.file_data.get(1.0, "end")
            try:
                with open(self.cur_file_path, 'w') as f:
                    f.write(data)
            except FileNotFoundError:
                text = "\nNo such file or directory.\n"
                mb.showerror(title="Error", message=text)
            else:
                # Уведомление об успешном действии с файлом
                text = "File {0} has been saved.".format(self.cur_file_name)
                mb.showinfo(title="Info", message=text)
                # Обновляем информацию о файле
                self.info_file(self.cur_file_path)


def app_info():
    """Показываем информацию об программе."""
    output = "\nAbout program.\n"
    mb.showinfo(title="About", message=output)


def app_exit():
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
        y = (screen_height / 2) - (height / 2)
    toplevel.geometry('+%d+%d' % (x, y))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    window_center(root)
    root.mainloop()
