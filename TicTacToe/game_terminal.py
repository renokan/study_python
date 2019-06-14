"""
Game "Tic-tac-toe" (terminal).

Игра "Крестики-нолики".
    Условия игры:
        1. Пользователь должен ввести кол-во игроков - 1 или 2.
        2. Показывается игровое поле с подсказками, пользователь делает ход.
        3. Показывается игровое поле и ход игрока, далее
        4.1. Если игра с компьютером - он делает ход и показывается куда походил
        4.2. Если игра с другим игроком - он должен сделать ход
        5. Алгоритм повторяется пока
        А. Или заканчиваются свободные поля
        Б. Кто-то выигрывает - Вы или компьютер / второй игрок

    Особенности реализации: компьютер играет по-умному.
        1. Он первым своим ходом пытается занять центр поля.
        2. Он старается предсказать ваше выигрышное поле и занять его.
        3. Он ищет свои выигрышные поля и если такие есть - ходит туда.
"""
import random
import time
import sys

# Это игровое поле
game_field = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]
              ]


def input_gamers():
    """Выбор кол-ва игроков. Проверка на корректность."""
    while True:
        try:
            # Спрашиваем у пользователя с кем он хочет играть
            x = input("\n\tEnter the number of players - 1 or 2: ")
        except KeyboardInterrupt:
            # Отлавливаем нажатие Ctrl + C
            print("\n\n\tOk. Game over.\n")
            sys.exit()
        else:
            # Если введены корректные данные - 1 или 2, тогда
            if x in ['1', '2']:
                return int(x)  # Всё получилось, выбор сделан. Завершаем цикл
            else:
                continue


def show_fields():
    """Показываем поле для игры. С пояснениями."""
    print()  # Пробел перед выводом поля
    for line in game_field:
        result = [line[:], line[:]]
        for x in range(len(line)):
            if isinstance(line[x], int):
                result[0][x] = ' '
                result[1][x] = str(line[x])
            else:
                result[1][x] = ' '
        field_l = " | ".join(result[0])
        field_r = " | ".join(result[1])
        print("\t {0}  {2}  {1}".format(field_l, field_r, " " * 5))
        # Горизонтальные разделительные лини под первым и вторым рядами
        if game_field.index(line) != 2:
            print("\t{0} {1} {0}".format("—" * 11, " " * 5))


def free_field():
    """Ищем свободные поля для записи."""
    result = []
    for line in game_field:
        result.extend([x for x in line if x in range(1, 10)])
    return result


def input_field():
    """Ввод данных пользователем. Проверки на корректность."""
    while True:
        try:
            # Спрашиваем у пользователя какое поле он хочет заполнить
            x_text = "{} must input number from".format(user_go)
            x_numbers = ", ".join([str(x) for x in free_field()])
            x = input("\n\t{0} {1!r}: ".format(x_text, x_numbers))
            # Пробуем введенный параметр привести к целому числу
            x = int(x)
        except KeyboardInterrupt:
            # Отлавливаем нажатие Ctrl + C
            print("\n\n\tOk. Game over.\n")
            sys.exit()
        except ValueError:
            # Если тип не подходящий (буквы) - продолжаем спрашивать число
            continue
        else:
            # Если получилось число, проверяем на соответствие диапазону
            if x in free_field():
                return x  # Всё получилось, выбор сделан. Завершаем цикл
            else:
                # Если это ноль или больше 9 - продолжаем спрашивать
                continue


def random_field():
    """Случайный выбор поля компьютером."""
    return random.choice(free_field())


def predict_win(xo=None):
    """Предсказать выигрышное поле."""
    # Есть 8 выигрышных комбинаций - 3 по горизонтали, 3 по вертикали и крест
    xy = game_field[:]  # Для краткости записи
    win_list = [[xy[0][0], xy[0][1], xy[0][2]],
                [xy[1][0], xy[1][1], xy[1][2]],
                [xy[2][0], xy[2][1], xy[2][2]],
                [xy[0][0], xy[1][0], xy[2][0]],
                [xy[0][1], xy[1][1], xy[2][1]],
                [xy[0][2], xy[1][2], xy[2][2]],
                [xy[0][0], xy[1][1], xy[2][2]],
                [xy[2][0], xy[1][1], xy[0][2]]
                ]

    # Перебираем список выигрышных комбинаций
    for win in win_list:
        # Ищем комбинацию, где уже два поля заполнены, если такое есть
        if win.count(xo) == 2:
            for x in win:
                # Ищем цифру и выводим её
                if isinstance(x, int):
                    return x


def effective_step():
    """Стараемся делать эффективные ходы, хотя и рандомайзом."""
    free_fields = free_field()
    if len(free_fields) > 7:
        # Компьютеру нужно сделать свой первый ход, стараемся занять центр
        if 5 in free_fields:
            return 5
        else:
            return random_field()
    elif len(free_fields) > 5:
        # Компьютеру нужно сделать второй ход
        # 1. Пробуем мешать сопернику, предсказав его выигрышное поле
        # 2. Если такого нет - делаем случайный ход
        if predict_win(xo_wait):
            return predict_win(xo_wait)
        else:
            return random_field()
    else:
        # Компьютеру нужно сделать остальные ходы
        # 1. Ищем своё выигрышное поле
        # 2. Пробуем мешать сопернику, предсказав его выигрышное поле
        # 3. Если такого нет - делаем случайный ход
        if predict_win(xo_go):
            return predict_win(xo_go)
        elif predict_win(xo_wait):
            return predict_win(xo_wait)
        else:
            return random_field()


def rewrite_field(f_index=None, f_value=None):
    """Перезаписываем поле по индексу (номеру в таблице), нужным значением."""
    # [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]
    for y in range(len(game_field)):
        for x in range(len(game_field[y])):
            if game_field[y][x] == f_index:
                game_field[y][x] = f_value


def check_win():
    """Проверка выигрышных комбинаций или кол-ва свободных полей."""
    # Есть 8 выигрышных комбинаций - 3 по горизонтали, 3 по вертикали и крест
    xy = game_field[:]  # Для краткости записи
    win_list = [[xy[0][0], xy[0][1], xy[0][2]],
                [xy[1][0], xy[1][1], xy[1][2]],
                [xy[2][0], xy[2][1], xy[2][2]],
                [xy[0][0], xy[1][0], xy[2][0]],
                [xy[0][1], xy[1][1], xy[2][1]],
                [xy[0][2], xy[1][2], xy[2][2]],
                [xy[0][0], xy[1][1], xy[2][2]],
                [xy[2][0], xy[1][1], xy[0][2]]
                ]

    # Если есть хоть одна выигрышная комбинация, тогда...
    for win in win_list:
        if win.count(xo_go) == 3:
            return ("Winner {}.".format(user_go), "Game over.")

    # Если выигрышных комбинаций нет и закончились свободные ячейки, тогда...
    if len(free_field()) == 0:
        return ("Last step. No winner.", "Game over.")


# ------------------------
# --- Логика программы ---
# ------------------------

if __name__ == '__main__':

    # Первый ход делаете вы
    user_go = 'You'
    xo_go = 'X'

    # Кто играет? Вы и компьютер или два человека между собой
    gamers = input_gamers()
    if gamers == 2:
        user_wait = 'User 1'
        step_type = 'input'
    else:
        user_wait = 'Computer'
        step_type = 'random'
    xo_wait = 'O'

    print("\n\tBeginning of the game. You and {}.".format(user_wait))

    while True:
        # Отображаем поле для игры
        show_fields()

        # Кто-то делает ход
        if user_go == 'You':
            # Запрашиваем нужное поле
            number_field = input_field()
        else:
            if step_type == 'input':
                # Запрашиваем у второго игрока, когда его очередь, нужное поле
                number_field = input_field()
            else:
                # Компьютер ждёт 1 секунду
                time.sleep(1)

                # и делает ход
                number_field = effective_step()

        # Записываем в нужно поле крестик/нолик
        rewrite_field(number_field, xo_go)

        # Пишем кто и как походил на игровом поле
        print("\n\t{0} makes move {1} -> {2}".format(user_go, xo_go, number_field))

        # Проверка на завершение игры
        if check_win():
            # Показываем поле последний раз
            show_fields()

            # Печатаем итог игры и выходим
            print("\n\t{0[0]} {0[1]}\n".format(check_win()))

            break  # Завершаем цикл с игрой

        # Меняем очередность хода и крестик-нолик
        user_go, user_wait = user_wait, user_go
        xo_go, xo_wait = xo_wait, xo_go

    # The END / Конец.
