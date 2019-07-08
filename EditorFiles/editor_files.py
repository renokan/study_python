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

При каждом действии, связанным с модификацией файла, справшивает у пользователя.
"""

import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as ld
import os
import time


class App:
    """Это класс с данными программы."""

    def __init__(self, root):
        """Что делаем при инициализации класса."""
        self.root = root
        self.app_create()
        self.reg_directory()
        self.reg_activate()
        self.reg_data()
        self.reg_info()
        self.reg_action()

    def app_create(self):
        """Конфигурируем окно программы."""
        # width = 480
        # height = 600
        # Название и фон
        self.root.title('Editor files')
        self.root.configure(background='white')
        self.root.resizable(True, False)
        # Размеры экрана
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # # Центрируем положение
        # x = (screen_width / 2) - (width / 2)
        # y = (screen_height / 2) - (height / 1.4)
        # self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        # self.root.resizable(True, True)
        # Меню
        top_menu = tk.Menu(self.root)
        self.root.config(menu=top_menu)
        top_menu.add_command(label="About", command=app_info)
        top_menu.add_command(label="Exit", command=app_exit)

    def reg_directory(self):
        """Выводим блок - текущая директория."""
        cur_dir = os.getcwd()
        self.reg_dir = tk.Frame(self.root, width=464, height=70, bg="white")
        self.reg_dir.pack(fill="x")

        self.dir_label = tk.Label(self.reg_dir, text="Current directory:", bg="white", bd=0)
        self.dir_btn = tk.Button(self.reg_dir, text="Change", command=self.change_dir)
        self.dir_info = tk.Label(self.reg_dir, text=cur_dir, bg="white", bd=0)

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
        self.file_data = tk.Text(self.reg_file, height=12, bg="gray80", fg='black', wrap="word")
        self.file_data.pack(fill="x")
        # scroll = tk.Scrollbar(self.reg_file, command=self.file_data.yview)
        # scroll.pack(side="left", fill="y")
        # self.file_data.config(yscrollcommand=scroll.set)

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
        new_dir = ld.askdirectory()
        if new_dir:
            os.chdir(new_dir)
            self.dir_info.configure(text=new_dir)

    def create_file(self):
        """Создаем новый файл."""
        name = self.file_name.get()
        if name:
            dir = os.getcwd()
            path_to_file = dir + "/" + name
            try:
                with open(path_to_file, 'x') as f:
                    data = self.file_data.get(1.0, "end")
                    if data:
                        f.write(data)
            except FileExistsError:
                text = "\nThis file already exists.\n"
                mb.showerror(title="Error", message=text)
            except FileNotFoundError:
                text = "\nNo such file or directory.\n"
                mb.showerror(title="Error", message=text)
            else:
                text = "\nFile {0} successfully created.\n".format(name)
                mb.showinfo(title="New file", message=text)
                self.info_file(path_to_file)
        else:
            text = "\nMissing file name.\n"
            mb.showerror(title="Error", message=text)

    def load_file(self):
        """Загружаем файл."""
        path_to_file = ld.askopenfilename(initialdir=os.getcwd(), title="Choose a file", filetypes=(("TXT files", "*.txt"), ("all files", "*.*")))
        if path_to_file:
            try:
                with open(path_to_file) as f:
                    temp = f.read()
            except Exception:
                text = "\nError loading file.\n"
                mb.showerror(title="Error load", message=text)
            else:
                self.file_data.delete(1.0, "end")
                self.file_data.insert(1.0, temp)
                self.file_name.delete(0, "end")
                self.file_name.insert(0, path_to_file.split(os.sep)[-1])
                self.info_file(path_to_file)
        # window_center(root)

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

        self.time_info.config(text=file_time)
        self.size_info.config(text=file_size)

        self.save_btn.config(state="active")
        self.del_btn.config(state="active")

        self.cur_file = path_to_file

    def del_file(self):
        """Удаляем файл."""
        name = self.cur_file.split(os.sep)[-1]
        text = "Delete file {0}?".format(name)
        answer = mb.askyesno(title="Delete", message=text)
        if answer is True:
            os.remove(self.cur_file)
            self.cur_file = ""

            text = "File {0} has been deleted.".format(name)
            mb.showinfo(title="Info", message=text)

            self.file_name.delete(0, "end")
            self.file_data.delete(1.0, "end")
            self.time_info.config(text="")
            self.size_info.config(text="")

            self.save_btn.config(state="disabled")
            self.del_btn.config(state="disabled")

    def save_file(self):
        """Сохраняем содержимое файла."""
        name = self.cur_file.split(os.sep)[-1]
        text = "Save file {0}?".format(name)
        answer = mb.askyesno(title="Save", message=text)
        if answer is True:
            data = self.file_data.get(1.0, "end")
            try:
                with open(self.cur_file, 'w') as f:
                    f.write(data)
            except FileNotFoundError:
                text = "\nNo such file or directory.\n"
                mb.showerror(title="Error", message=text)
            else:
                text = "File {0} has been saved.".format(name)
                mb.showinfo(title="Info", message=text)
                self.info_file(self.cur_file)


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
