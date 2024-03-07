cells = [['·'] * 8 for i in range(8)]  # -> основание доски, поле боя
whites = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']  # -> белые фигуры
blacks = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']  # -> черные фигуры
empty_check = ['r', 'n', 'b', 'q', 'k', 'R', 'N', 'B', 'Q', 'K', 'p',
               'P']  # -> чек на то, пустая ли клетка, из которой совершается ход
dictionary = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
              'h': 7}  # -> словарь для итерации по доске и перевода изначального ввода в элементы списка cells


def file_transcript(file):
    with open(file) as f:
        f = f.readlines()
        steps = [line[2:][2:].strip().split(' ') for line in f]
        return steps[:-1]


moves = []
last_step = []


def checkmate():
    check_mate = ''
    for rows in cells:
        for figures in rows:
            check_mate += figures
    if 'K' not in check_mate:
        print('\033[40mПобеда черных\033[0m')
        return True
    elif 'k' not in check_mate:
        print('\033[40mПобеда белых\033[0m')
        return True
    else:
        return None


def record(moves_result, last_step):
    moves_result.append(last_step)
    with open('recorded.txt', 'w+') as f:
        for els in moves_result:
            f.write(' '.join(str(x) for x in els))
            f.write('\n')
        f.write('Конец игры')


for iterator3 in range(8):  # -> просто рисуем доску, в последствии она изменяется
    cells[0][iterator3] = blacks[iterator3]
    cells[1][iterator3] = 'p'
    cells[6][iterator3] = 'P'
    cells[7][iterator3] = whites[iterator3]


def draw_board(cells):
    print('\033[35m ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '\033[0m')
    for iterator1 in range(8):
        print(str(8 - iterator1), end=' ')
        [print(cells[iterator1][iterator2], end=' ') for iterator2 in range(8)]
        print(str(8 - iterator1))
    print('\033[35m ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '\033[0m')


def checkmate_record(cells):
    check_mate = ''
    for rows in cells:
        for figures in rows:
            check_mate += figures
    if 'K' not in check_mate:
        print('\033[40mПобеда черных\033[0m')
        return True
    elif 'k' not in check_mate:
        print('\033[40mПобеда белых\033[0m')
        return True
    else:
        return None


def conversion(start, stop):
    return 8 - int(start[1]), dictionary[start[0]], 8 - int(stop[1]), dictionary[stop[0]]  # -> (from1, from2, to1,
    # to2) конвертация из пользовательского во внутреннее представление


def move(step=None):
    starts_rec_check = []
    if step == None:
        step = 1
    while True:
        if step % 2 != 0:  # -> для определения хода : ч/б
            print(f'\033[32m {step}\033[0m\033[1m Ход белых: \033[0m')
        else:
            print(f'\033[32m {step}\033[0m\033[1m Ход черных: \033[0m')
        draw_board(cells)  # -> рисую доску
        start = input('\033[3mИз какой клетки сделать ход? \033[0m ').lower()
        starts_rec_check.append(start)
        if len(start) != 2:  # -> проверка на корректность введенной клетки отсюда:
            print('\033[31mВведите корректную клетку. Если вы ввели "запись", запись игры начата!\033[0m')
        elif start[0].lower() < 'a' or start[0].lower() > 'h':
            print(f' {start[0]} не в промежутке a - h')
        elif int(start[1]) < 1 or int(start[1]) > 8:
            print(f'\033[31m{start[1]} не в промежутке 1 - 8\033[0m')  # -> до этого момента и в некоторых случаях далее
        else:
            stop = input('\033[3mВ какую клетку?  \033[0m').lower()
            if len(stop) != 2:
                print('\033[31mВведите корректную клетку\033[0m')
            from_row = conversion(start, stop)[0]
            from_col = conversion(start, stop)[1]
            to_row = conversion(start, stop)[2]
            to_col = conversion(start, stop)[3]
            if cells[from_row][from_col] not in empty_check:
                print('\033[31mВы выбрали пустую клетку, повторите ход еще раз \033[0m')
            else:
                if step % 2 == 0 and cells[from_row][from_col].isupper():
                    print('\033[31mВы выбрали чужую фигуру, повторите ход еще раз \033[0m')
                elif step % 2 != 0 and cells[from_row][from_col].islower():
                    print('\033[31mВы выбрали чужую фигуру, повторите ход еще раз \033[0m')
                else:
                    if (cells[from_row][from_col]).lower() == 'p':  # конкретно ход
                        if pawn(from_row, from_col, to_row, to_col, cells[from_row][from_col]):
                            step += 1
                            moves.append('P' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('P' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
                    elif (cells[from_row][from_col]).lower() == 'n':
                        if knight(from_row, from_col, to_row, to_col, cells[from_row][from_col],
                                  cells[to_row][to_col]):
                            step += 1
                            moves.append('N' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('N' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
                    elif (cells[from_row][from_col]).lower() == 'r':
                        if rook(from_row, from_col, to_row, to_col, cells[from_row][from_col],
                                cells[to_row][to_col], moves_result):
                            step += 1
                            moves.append('R' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('R' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
                    elif (cells[from_row][from_col]).lower() == 'b':
                        if bishop(from_row, from_col, to_row, to_col, cells[from_row][from_col],
                                  cells[to_row][to_col]):
                            step += 1
                            moves.append('B' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('B' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
                    elif (cells[from_row][from_col]).lower() == 'q':
                        if queen(from_row, from_col, to_row, to_col, cells[from_row][from_col],
                                 cells[to_row][to_col]):
                            step += 1
                            moves.append('Q' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('Q' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
                    elif (cells[from_row][from_col]).lower() == 'k':
                        if king(from_row, from_col, to_row, to_col, cells[from_row][from_col],
                                cells[to_row][to_col]):
                            step += 1
                            moves.append('K' + start)
                            moves.append(stop)
                            if checkmate():
                                last_step.append(str(step) + '.')
                                last_step.append('K' + start)
                                last_step.append(stop)
                                for els in starts_rec_check:
                                    if els == 'запись' or els == 'Запись':
                                        record(moves_result, last_step)
                                        return True
                                return True
            k = 1
            moves_result = [[moves[i], moves[i + 1]] for i in
                            range(0, len(moves), 2)]  # просто запись игры, потом трогать
            for els in moves_result:
                els.insert(0, str(k) + '.')
                k += 1


def pawn(from_row, from_col, to_row, to_col,
         b_or_w):  # print(cells[6]) -> ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'] пешка
    if (b_or_w.isupper() and from_row < to_row) or (b_or_w.islower() and from_row > to_row):
        print('\033[31mВведите корректную клетку\033[0m')
        return None
    elif from_col == to_col:
        if from_row == 1 or from_row == 6:
            if 1 <= abs(from_row - to_row) <= 2 and cells[to_row][to_col] == '·':
                cells[to_row][to_col] = cells[from_row][from_col]
                cells[from_row][from_col] = '·'
                return True
            else:
                print('\033[31mВведите корректную клетку\033[0m')
                return None
        else:
            if abs(from_row - to_row) == 1 and cells[to_row][to_col] == '·':
                cells[to_row][to_col] = cells[from_row][from_col]
                cells[from_row][from_col] = '·'
                return True
            else:
                print('\033[31mВведите корректную клетку\033[0m')
    elif abs(from_row - to_row) == 1 and (abs(from_col - to_col == 1) or (from_col + 1 == to_col)) and (
            (cells[from_row][from_col].islower() != cells[to_row][to_col].islower()) or (
            cells[from_row][from_col].isupper() != cells[to_row][to_col].isupper())) and cells[to_row][
        to_col] != '·':  # бить по диагонали
        cells[to_row][to_col] = cells[from_row][from_col]
        cells[from_row][from_col] = '·'
        print('eba')
        return True
    else:
        print('\033[31mВведите корректную клетку\033[0m')
        print('aaa')
        return None


def knight(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):  # конь cells[0][4], cells[7][4]
    if (b_or_w1.isupper() == b_or_w2.isupper() or b_or_w1.islower() == b_or_w2.islower()) and (b_or_w2 != '·'):
        print('\033[31mВведите корректную клетку\033[0m')
        return None
    elif (from_row - to_row == 2 and from_col - to_col == 1) or (
            from_row - to_row == 2 and from_col - to_col == -1) or (
            from_row - to_row == 1 and from_col - to_col == 2) or (
            from_row - to_row == 1 and from_col - to_col == -2) or (
            from_row - to_row == -1 and from_col - to_col == 2) or (
            from_row - to_row == -1 and from_col - to_col == -2) or (
            from_row - to_row == -2 and from_col - to_col == 1) or (
            from_row - to_row == -2 and from_col - to_col == -1):
        cells[to_row][to_col] = cells[from_row][from_col]
        cells[from_row][from_col] = '·'
        return True
    else:
        print('\033[31mВы пытаетесь сделать невозможный ход\033[0m')
        return None


def rook(from_row, from_col, to_row, to_col, b_or_w1,
         b_or_w2,
         moves_result=''):  # ладья не перепрыгивает фигуры, ходит _ или | на любое к-во клеток до встречи с какой-либо другой фигурой
    stringmoves = ''

    if (b_or_w1.isupper() == b_or_w2.isupper() or b_or_w1.islower() == b_or_w2.islower()) and (b_or_w2 != '·') and (
            b_or_w2.lower() != 'k'):
        print('\033[31mНельзя пойти в свою фигуру\033[0m')
        return None
    elif (to_row < from_row and to_col == from_col) or (to_row < from_row and to_col == from_col) or (
            to_row == from_row and to_col < from_col) or (to_row == from_row and to_col > from_col):
        if to_row < from_row:
            if all(cells[rows][to_col] == '·' for rows in range(from_row - 1, to_row, -1)):
                cells[to_row][to_col] = cells[from_row][from_col]
                cells[from_row][from_col] = '·'
                return True
            else:
                print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                return None
        if to_row > from_row:
            if all(cells[rows][to_col] == '·' for rows in range(from_row + 1, to_row)):
                cells[to_row][to_col] = cells[from_row][from_col]
                cells[from_row][from_col] = '·'
                return True
            else:
                print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                return None
        if to_col > from_col:
            if all(cells[to_row][cols] == '·' for cols in range(from_col + 1, to_col)):
                if b_or_w2.lower() == 'k' and len(moves_result) > 0:
                    print('aa')
                    for el in moves_result:
                        for els in el:
                            stringmoves += els
                    if 'k' in stringmoves or 'r' in stringmoves:
                        print('\033[31mбыло движение\033[0m')
                        print(stringmoves)
                        return None
                    cells[from_row][3] = cells[from_row][from_col]
                    cells[from_row][from_col] = '·'
                    cells[from_row][2] = b_or_w2
                    cells[to_row][to_col] = '·'
                    return True  # длинная рокировка
                else:
                    cells[to_row][to_col] = cells[from_row][from_col]
                    cells[from_row][from_col] = '·'
                    return True
            else:
                print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                return None
        if to_col < from_col:
            if all(cells[to_row][cols] == '·' for cols in range(from_col - 1, to_col, -1)):
                if b_or_w2.lower() == 'k' and len(moves_result) > 0:
                    print('aa')
                    for el in moves_result:
                        for els in el:
                            stringmoves += els
                    if 'k' in stringmoves or 'r' in stringmoves:
                        print('\033[31mбыло движение\033[0m')
                        print(stringmoves)
                        return None
                    cells[from_row][5] = cells[from_row][from_col]
                    cells[from_row][from_col] = '·'
                    cells[from_row][6] = b_or_w2
                    cells[to_row][to_col] = '·'
                    return True  # короткая рокировка
                else:
                    cells[to_row][to_col] = cells[from_row][from_col]
                    cells[from_row][from_col] = '·'
                    return True
            else:
                print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                return None
    else:
        print('\033[31mВведите корректную клетку\033[0m')
        return None


def bishop(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):
    if (b_or_w1.isupper() == b_or_w2.isupper() or b_or_w1.islower() == b_or_w2.islower()) and (b_or_w2 != '·'):
        print('\033[31mНельзя пойти в свою фигуру\033[0m')
        return None
    check_cords = {}
    xx = []
    yy = []
    if abs(from_row - to_row) == abs(from_col - to_col):
        if to_row < from_row and to_col > from_col:  # вверх вправо
            for x in range(from_row - 1, to_row, -1):
                xx.append(x)
            for y in range(from_col + 1, to_col):
                yy.append(y)
            for i in range(len(xx)):
                check_cords[xx[i]] = yy[i]
            check_cords = tuple(check_cords.items())
            for els in check_cords:
                if cells[els[0]][els[1]] != '·':
                    print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                    return None
            cells[to_row][to_col] = cells[from_row][from_col]
            cells[from_row][from_col] = '·'
            return True
        elif to_row < from_row and to_col < from_col:  # вверх влево
            for x in range(from_row - 1, to_row, -1):
                xx.append(x)
            for y in range(from_col - 1, to_col, -1):
                yy.append(y)
            for i in range(len(xx)):
                check_cords[xx[i]] = yy[i]
            check_cords = tuple(check_cords.items())
            for els in check_cords:
                if cells[els[0]][els[1]] != '·':
                    print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                    return None
            cells[to_row][to_col] = cells[from_row][from_col]
            cells[from_row][from_col] = '·'
            return True
        elif to_row > from_row and to_col < from_col:  # вниз влево
            for x in range(from_row + 1, to_row):
                xx.append(x)
            for y in range(from_col - 1, to_col, -1):
                yy.append(y)
            for i in range(len(xx)):
                check_cords[xx[i]] = yy[i]
            check_cords = tuple(check_cords.items())
            for els in check_cords:
                if cells[els[0]][els[1]] != '·':
                    print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                    return None
            cells[to_row][to_col] = cells[from_row][from_col]
            cells[from_row][from_col] = '·'
            return True
        elif to_row > from_row and to_col > from_col:  # вниз вправо
            for x in range(from_row + 1, to_row):
                xx.append(x)
            for y in range(from_col + 1, to_col):
                yy.append(y)
            for i in range(len(xx)):
                check_cords[xx[i]] = yy[i]
            check_cords = tuple(check_cords.items())
            for els in check_cords:
                if cells[els[0]][els[1]] != '·':
                    print('\033[31mПопытка перепрыгнуть через фигуру\033[0m')
                    return None
            cells[to_row][to_col] = cells[from_row][from_col]
            cells[from_row][from_col] = '·'
            return True
        else:
            print('\033[31mХод не по правилам\033[0m')
            return None


def queen(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):
    if (b_or_w1.isupper() == b_or_w2.isupper() or b_or_w1.islower() == b_or_w2.islower()) and (b_or_w2 != '·'):
        print('\033[31mНельзя пойти в свою фигуру\033[0m')
        return None
    if abs(from_row - to_row) == abs(from_col - to_col):
        if bishop(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):
            return True
        else:
            return None
    elif (to_row < from_row and to_col == from_col) or (to_row < from_row and to_col == from_col) or (
            to_row == from_row and to_col < from_col) or (to_row == from_row and to_col > from_col):
        if rook(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):
            return True
        else:
            return None
    else:
        print('\033[31mВведите корректную клетку\033[0m')
        return None


def king(from_row, from_col, to_row, to_col, b_or_w1, b_or_w2):
    if (b_or_w1.isupper() == b_or_w2.isupper() or b_or_w1.islower() == b_or_w2.islower()) and (b_or_w2 != '·') and (
            b_or_w2.lower != 'r'):
        print('\033[31mНельзя пойти в свою фигуру\033[0m')
        return None
    if abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
        cells[to_row][to_col] = cells[from_row][from_col]
        cells[from_row][from_col] = '·'
        return True
    else:
        print('\033[31mНеверный ход\033[0m')
        return None


def rec_move(moves_to_read, pokakoy_xod, cells=None):
    if cells == None:
        cells = [['·'] * 8 for i in range(8)]
    for iterator_new in range(8):
        cells[0][iterator_new] = blacks[iterator_new]
        cells[1][iterator_new] = 'p'
        cells[6][iterator_new] = 'P'
        cells[7][iterator_new] = whites[iterator_new]
    for i in range(0, pokakoy_xod):
        start, stop = moves_to_read[i][0], moves_to_read[i][1]
        from_row = conversion(start, stop)[0]
        from_col = conversion(start, stop)[1]
        to_row = conversion(start, stop)[2]
        to_col = conversion(start, stop)[3]
        cells[to_row][to_col] = cells[from_row][from_col]
        cells[from_row][from_col] = '·'
    draw_board(cells)
    if pokakoy_xod == len(moves_to_read):
        checkmate_record(cells)
        return True


def move_using_the_record(moves_to_read):
    current_move_index = 1
    print(f'\033[32m {current_move_index}\033[0m')
    rec_move(moves_to_read, current_move_index)
    while True:
        user_input = input('')
        if user_input == 'next' or user_input == 'дальше' or user_input == 'вперед':
            current_move_index += 1
            print(f'\033[32m {current_move_index}\033[0m')
            if rec_move(moves_to_read, current_move_index):
                return True
        elif user_input == 'prev' or user_input == 'previous' or user_input == 'пред' or user_input == 'раньше' or user_input == 'назад':
            if current_move_index == 0:
                return False
            else:
                current_move_index -= 1
                print(f'\033[32m {current_move_index}\033[0m')
                rec_move(moves_to_read, current_move_index)
        else:
            rec_move(moves_to_read, current_move_index, cells)
            if move(current_move_index + 1):
                print('\033[32mКонец игры\033[0m')


to_read_or_not_to_read = input('Читаем игру из файла? Если да, введите название .txt файла с нотацией игры: ')

if to_read_or_not_to_read[-3:] == 'txt':
    moves_to_read = file_transcript(to_read_or_not_to_read)
    if move_using_the_record(moves_to_read):
        print('\033[32mКонец игры\033[0m')
    else:
        print('\033[31mНеверный ввод\033[0m')
else:
    if move():
        print('\033[32mКонец игры\033[0m')
