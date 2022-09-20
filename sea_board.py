import random
import os
import sys

size = 6

# Отображаем свое поле
# visable = True
# visable = False

# Отображаем  поле компьютера (в режиме отладки)
monitoring = False
monitoring = True

# набор меток для игрового поля
str_buffer = "☺"
str_ship = "■"
str_space = "."
str_hit = "x"
str_destroyed = "☻"
str_miss = "*"

# Устанавливаем набор кораблей [палубность,количество]
ships_list = [[3, 1], [2, 2], [1, 3]]


# ships_list = [[1, 2]]  для теста


# Класс игровое поле
class Board(object):
    axis_x_y = 0  # признак с какой оси начинаем выбор координат для случайной клетки

    def __init__(self):
        self.board = []
        self.destroyed = []
        self.ships_direct = []

    def create(self):
        for row in range(size):
            # print(row)
            self.board.append([str_space] * size)

    # Размещение кораблей на поле
    def arbitrary_ship(self):
        # max_ship = 0
        #  случайным образом размещаем на поле корабли
        for elem_ship in ships_list:
            # if elem_ship[0] > max_ship:
            # max_ship = elem_ship[0]
            for elem in range(elem_ship[0]):

                sign_ = True
                while sign_:
                    axis_x_y = random.randrange(2)
                    # Выбор начальной точки
                    # выбор по оси X
                    if axis_x_y == 0:
                        local_x = random.randrange(size)
                        local_y = random.randrange(size - (elem_ship[1] - 1))
                    else:
                        # выбор по оси Y
                        local_x = random.randrange(size - (elem_ship[1] - 1))
                        local_y = random.randrange(size)

                    # Формирование кораблей
                    indexs = 0
                    for check in range(elem_ship[1]):
                        if axis_x_y == 0 and self.board[local_x][local_y + indexs] != str_space:
                            continue
                        elif axis_x_y == 1 and self.board[local_x + indexs][local_y] != str_space:
                            continue
                        indexs += 1
                        if indexs == elem_ship[1]:
                            sign_ = False

                            indexs = 0
                            current_ship = []
                            for elem_mark in range(elem_ship[1]):
                                if axis_x_y == 0:
                                    self.board[local_x][local_y + indexs] = str_ship
                                    current_ship.append([local_x, local_y + indexs])
                                else:
                                    self.board[local_x + indexs][local_y] = str_ship
                                    current_ship.append([local_x + indexs, local_y])
                                indexs += 1
                            self.destroyed.append(current_ship)

                            for point in current_ship:
                                for point_var in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                                    point_x = point[0] + point_var[0]
                                    point_y = point[1] + point_var[1]
                                    if point_y in range(size) and point_x in range(size):
                                        if self.board[point_x][point_y] == str_space:
                                            self.board[point_x][point_y] = str_buffer
        # self.ships_direct = ([str_space] * max_ship)

    # обновляем метки на доске после выстрела
    def update_ship(self, ship):
        for elem_update in ship:
            # Проверяем соседние координаты
            for point_var in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                point_x = elem_update[0] + point_var[0]
                point_y = elem_update[1] + point_var[1]
                if point_y in range(size) and point_x in range(size):
                    if self.board[point_x][point_y] == str_buffer:
                        self.board[point_x][point_y] = str_miss
                    elif self.board[point_x][point_y] == str_hit:
                        self.board[point_x][point_y] = str_destroyed


# Вывод на консоль игровое поле
def print_boards():
    print("\nВаше игровое поле" + " " * 2 + "Поле компьютера")
    print("  Y " + (" ".join(str(i) for i in list(range(size)))), end=("  " * 2))
    print("Y " + (" ".join(str(i) for i in list(range(size)))))
    print("X  " + (" |" * size), end=(" " * 2))
    print("X  " + (" |" * size))
    n = 0
    for i in range(size):

        print(str(n) + " - " + " ".join(str(i) for i in player.board[n]).replace(str_buffer, str_space),
              end=(" " * 2))
        # Отображение кораблей на  поле компьютера для тестирования
        if monitoring:
            print(str(n) + " - " + " ".join(str(i) for i in comp.board[n]).replace(str_ship, str_space). \
                  replace(str_buffer, str_space))
        else:
            print(str(n) + " - " + " ".join(str(i) for i in comp.board[n]).replace(str_buffer, str_space). \
                  replace(str_buffer, str_space))

        n += 1


def press_ent():
    char_put = input(" Enter для продолжения,  либо  -9 для завершение программы ")
    if char_put == '-9':
        sys.exit(0)
    # quit


# Вывод статуса кораблей игроков
def print_board():
    print("\nКораблей у противника: " + str(len(comp.destroyed)) + ". ", end="")
    print("Ваших кораблей: " + str(len(player.destroyed)) + ".")


# Статус кораблей игроков
def state_of_ships(enemy):
    for d_ship in enemy.destroyed:
        damage = 0
        for elem in d_ship:
            if enemy.board[elem[0]][elem[1]] == str_hit:
                damage += 1
                if damage == len(d_ship):
                    enemy.update_ship(d_ship)
                    enemy.destroyed.remove(d_ship)
                    return True
    return False


# Случайные координаты (X,Y) для выстрела компьютером
def comp_pass():
    comp_guessing = True
    comp_repeat = False
    l = []
    while comp_guessing:
        # Поиск подбитых кораблей (реализовано для одной итерации)
        if len(comp.ships_direct) > 0:
            for elem_direct in range(len(comp.ships_direct)):
                for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0]):
                    point_x = comp_guess_x + buffer_point[0]
                    point_y = comp_guess_y + buffer_point[1]
                    if point_y in range(size) and point_x in range(size):
                        if player.board[point_x][point_y] not in [str_hit, str_miss]:
                            l.append([point_x, point_y])

                comp_int_ship = random.randrange(len(l))
                comp_guess_x = l[comp_int_ship][0]
                comp_guess_y = l[comp_int_ship][1]
                comp.ships_direct = []
        else:
            comp_guess_y = random.randrange(size)
            comp_guess_x = random.randrange(size)
        if player.board[comp_guess_x][comp_guess_y] == str_ship:
            player.board[comp_guess_x][comp_guess_y] = str_hit
            if state_of_ships(player):
                print("\nКомпьютер уничтожил ваше судно (X: %s, Y: %s)." % (comp_guess_x, comp_guess_y), end=" ")
                if len(player.destroyed) != 0:
                    print("   Ваш выстрел!")
                    comp.ships_direct = []
                else:
                    # state_of_ships(player)
                    break
            else:
                print("\nКомпьютер повредил ваше судно (X: %s, Y: %s)." % (comp_guess_x, comp_guess_y),
                      "  Компьютер повторит выстрел!")
                print_boards()
                comp.ships_direct.append([comp_guess_x, comp_guess_y])
                continue
            break

        elif player.board[comp_guess_x][comp_guess_y] == str_space or player.board[comp_guess_x][
            comp_guess_y] == str_buffer:
            player.board[comp_guess_x][comp_guess_y] = str_miss
            print("\nКомпьютер выстрелил мимо (X: %s, Y: %s)." % (comp_guess_x, comp_guess_y), "  Ваш выстрел!")
            break
        else:
            continue


# Очистка консоли
def clear(message='', press=0):
    os.system('cls')
    print(message)
    if press != 0:
        press_ent()


# Вызов исключений
class MyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}'


# Начало игры
print('---------------------------------------------------------------------')
print('-------------------------ИГРА МОРСКОЙ БОЙ----------------------------')
print('---------------------------------------------------------------------')
print('              Играют два игрока на поле %s X %s . ' % (size, size))
print('           Корабли на поле располагаются случайным образом           ')
print('         3- однопалобных, 2 - двухпалобных, 1 - трехпалубный         ')
print('              Первым начинает  компьютер, следующий Игрок            ')
print('            Вводятся по очереди  координаты для выстрелов.           ')
print('    Если корабль поврежден, то предоставляется дополнительный выстрел')
print('---------------------------------------------------------------------')
# Формируем поле и корабли для Игрока
comp = Board()
comp.create()
comp.arbitrary_ship()

while True:
    clear('\nНачинаем новую игру\n', 1)
    player = Board()
    player.create()
    player.arbitrary_ship()
    print_boards()
    print("Для подтверждения расположения короблей на вашем поле нажмите любую клавишу, кроме 0 ")
    regenerate = input("Для изменения расположения кораблей, нажмите 0 ")
    if str(regenerate.lower()) == "0":
        continue
    else:
        break

# print("\nНачинаем новую игру\n")
# press_ent()

game = True
while game:
    clear(" ", 1)
    comp_pass()  # Выстрел компьютера
    print_boards()
    if len(player.destroyed) == 0:
        break

    sign_ = True
    while sign_:
        print_board()
        try:
            player_x = input("Выберите X (строка) для стрельбы: ")
            player_y = input("Выберите Y (столбец) для стрельбы: ")
            if not player_x.isdigit() or not player_y.isdigit():
                raise MyError(' Не верные координаты, повторите ввод!')
                continue

            player_x = int(player_x)
            player_y = int(player_y)

            if not (player_x in range(size)) or not (player_y in range(size)):
                # print("\nНекорректные координаты! Выберите другие")
                raise MyError(' Не верные координаты, повторите ввод!')
                continue

            elif comp.board[player_x][player_y] == str_ship:
                comp.board[player_x][player_y] = str_hit

                if state_of_ships(comp):
                    print("\nВы уничтожили судно компьютера! ", end=" ")
                    if len(comp.destroyed) != 0:
                        print(" Теперь выстрел компьютера!")
                else:
                    # raise MyError("\nВы повредили судно компьютера!  Повторите свой выстрел!")
                    print("\nВы повредили судно компьютера!  Повторите свой выстрел!", end=" ")
                    print_boards()
                    continue
                print_boards()
                break

            elif comp.board[player_x][player_y] == str_space or comp.board[player_x][player_y] == str_buffer:
                comp.board[player_x][player_y] = str_miss
                print("\nВы промахнулись! Теперь выстрел компьютера!", end=" ")
            else:
                print("\nВы уже стреляли по этим координатам, повторите выстрел! ")
                continue
            break
        except MyError as mr:
            print(mr)
            continue

    if len(player.destroyed) == 0:
        print("\nВы проиграли! ENTER - завершить игру")
        print_board()
        break

    if len(comp.destroyed) == 0:
        input("\nВы победили!  ENTER - завершить игру ")
        print_board()
        break

clear('\nКонец игре')