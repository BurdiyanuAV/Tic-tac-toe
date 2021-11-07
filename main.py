import pygame
import sys


# Функция для вывода сообщения о конце игры
def end_message(text, color, font, surface, background_color=(143, 192, 233), border_color=(33, 90, 136)):
    message = font.render(text, True, color)    # создаем поверхность с текстом
    # создаем вокруг поверхность "окошка"
    message_window = pygame.Surface((message.get_rect().width + 100, message.get_rect().height + 100))
    # создаем прямоугольник с центром в центре окошка (для текста)
    message_rect = message.get_rect(center=(message_window.get_rect().width / 2, message_window.get_rect().height / 2))
    # создаем прямоугольник с центром в центре экрана(surface) для окошка
    message_window_rect = message_window.get_rect(center=(surface.get_rect().width / 2, surface.get_rect().height / 2))
    message_window.fill(background_color)   # заполняем окошко цветом
    pygame.draw.rect(message_window, border_color, message_window.get_rect(), 15)   # рисуем окну рамку
    message_window.set_alpha(235)       # делаем окошко немного прозрачным
    message_window.blit(message, message_rect)      # прорисовываем надпись на окошке
    surface.blit(message_window, message_window_rect)   # прорисовываем окошко с надписью на поверхности


# Класс для игрового поля
class Board:
    def __init__(self, size, surface):
        self.size = size
        self.surface = surface
        self.width = self.surface.get_rect().width              # получаем ширину поверхности
        self.block_size = self.width // self.size               # вычисляем размер одного блока
        self.table = [[0] * size for i in range(size)]          # таблица с данными о заполнении поля
        self.draw_board()                                       # начальная прорисовка поля

    # добавление знака
    def place_sign(self, row, col, sign):
        self.table[row][col] = sign                                             # добавление в таблицу с данными
        # прорисовка
        if sign == 1:                                                           # если знак - крестик
            x1 = self.block_size * col + 10
            y1 = self.block_size * row + 10
            x2 = self.block_size * (col + 1) - 10
            y2 = self.block_size * (row + 1) - 10
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 3)
            x1 = self.block_size * (col + 1) - 10
            x2 = self.block_size * col + 10
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 3)
        elif sign == 2:                                                         # если знак - нолик
            r = self.block_size / 2 - 10
            x = self.block_size * col + self.block_size / 2
            y = self.block_size * row + self.block_size / 2
            pygame.draw.circle(self.surface, light_cyan, (x, y), r, 3)

    # Проверка ячейки на пустоту
    def spot_available(self, row, col):
        return self.table[row][col] == 0

    # проверка поля на заполненность
    def is_full(self):
        # если есть хоть один ноль в таблице - вернуть ложь, если нет - вернуть правду
        for row in range(self.size):
            for col in range(self.size):
                if self.table[row][col] == 0:
                    return False

        return True

    # Прорисовка поля
    def draw_board(self):
        self.surface.fill(blue_1)
        # border = pygame.draw.rect(self.surface, light_cyan, self.surface.get_rect(), self.margin)  # рамка
        for i in range(self.size - 1):                                          # цикл прорисовки линий
            # вертикальная линия
            x1 = x2 = self.block_size * (i + 1)
            y1 = 0
            y2 = self.width
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 1)
            # горизонтальная линия
            x1 = 0
            y1 = y2 = self.block_size * (i + 1)
            x2 = self.width
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 1)

    # функция проверки победы
    def win_check(self, length=3):

        # переменные для побед
        vertical_win = False
        horizontal_win = False
        right_diag_win = False
        left_diag_win = False

        # в этом массиве будет хранится '0', если ячейка не является началом победной линии и
        # код, если не является
        win_table = [[''] * self.size for i in range(self.size)]

        # Поиск вертикальных побед
        for col in range(self.size):                    # по всем столбцам
            for row in range(self.size - length + 1):   # проверяем каждую ячейку на победу "внизу"
                if self.table[row][col] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[row][col]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек внизу
                        if x == self.table[row+i][col]:     # если ячейки снизу совпадают
                            vertical_win = True        # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            vertical_win = False
                            break
                    if vertical_win:                    # если зафиксирована победа
                        win_table[row][col] += 'v'       # зафиксировать в таблице

        # Поиск горизонтальных побед
        for row in range(self.size):                    # по всем строкам
            for col in range(self.size - length + 1):   # проверяем каждую ячейку на победу "справа"
                if self.table[row][col] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[row][col]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек справа
                        if x == self.table[row][col+i]:     # если ячейки справа совпадают
                            horizontal_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            horizontal_win = False
                            break
                    if horizontal_win:
                        win_table[row][col] += 'h'       # зафиксировать в таблице

        # Поиск победы на диагонали в правую сторону
        for row in range(self.size - length + 1):
            for col in range(self.size - length + 1):   # проверяем каждую ячейку на диагональ справа-снизу
                if self.table[row][col] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[row][col]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек справа-снизу
                        if x == self.table[row+i][col+i]:     # если ячейки справа-снизу совпадают
                            right_diag_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            right_diag_win = False
                            break
                    if right_diag_win:
                        win_table[row][col] += 'rd'       # зафиксировать в таблице

        # Поиск победы на диагонали в левую сторону
        for row in range(self.size - length + 1):
            for col in range(length - 1, self.size):   # проверяем каждую ячейку на диагональ слева-снизу
                if self.table[row][col] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[row][col]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек слева-снизу
                        if x == self.table[row+i][col-i]:     # если ячейки слева-снизу совпадают
                            left_diag_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            left_diag_win = False
                            break
                    if left_diag_win:
                        win_table[row][col] += 'ld'       # зафиксировать в таблице

        return win_table                    # возврат таблицы с указанными победными ячейками

    # Прорисовка линии при победе
    def draw_win_line(self, col, row, win_type, length, line_width=5):
        # принимает позицию первой ячейки линии, длину и тип победы
        # определяются координаты концов линии в зависимости от типа победы
        # тип победы - строка с перечислением побед
        # если в строке есть определенное сочетание букв, то прорисовывается соответствующая линия
        if 'v' in win_type:
            x1 = col * self.block_size + self.block_size / 2
            y1 = row * self.block_size + 5
            x2 = x1
            y2 = y1 + self.block_size * length - 10
            pygame.draw.line(self.surface, black, (x1, y1), (x2, y2), line_width)
        if 'h' in win_type:
            x1 = col * self.block_size + 5
            y1 = row * self.block_size + self.block_size / 2
            x2 = x1 + self.block_size * length - 10
            y2 = y1
            pygame.draw.line(self.surface, black, (x1, y1), (x2, y2), line_width)
        if 'rd' in win_type:
            x1 = col * self.block_size + 5
            y1 = row * self.block_size + 5
            x2 = x1 + self.block_size * length - 10
            y2 = y1 + self.block_size * length - 10
            pygame.draw.line(self.surface, black, (x1, y1), (x2, y2), line_width)
        if 'ld' in win_type:
            x1 = (col+1) * self.block_size - 5
            y1 = row * self.block_size + 5
            x2 = x1 - self.block_size * length + 10
            y2 = y1 + self.block_size * length - 10
            pygame.draw.line(self.surface, black, (x1, y1), (x2, y2), line_width)


pygame.init()   # Инициализация pygame

# Переменные
# цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
darkgray = (169, 169, 169)
light_cyan = (224, 255, 255)
blue_1 = (102, 161, 210)

win_width = 600                    # ширина окна
win_height = 600                   # высота окна
FPS = 50                           # количество кадров, для определения задержки
font = pygame.font.SysFont(None, 25, bold=True)     # Определение объекта-шрифта

screen = pygame.display.set_mode((win_width, win_height))     # инициализация основного окна
pygame.display.set_caption('Крестики-нолики')                                   # надпись на окне

clock = pygame.time.Clock()         # инициализация объекта часов, используемого для задержки

# Предшествующие игре действия
board_size = 5
win_length = 4
game_board = Board(board_size, screen)       # создание объекта-поля для игры

player = 1                          # ходит первый игрок
board_is_active = True              # доска активирована
game_finished = False               # игра не закончена

# основной цикл игры
while True:
    # Цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # выход из программы
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:    # клик ЛКМ по окну
            if board_is_active:
                mouseX = event.pos[0]                   # получаем координаты клика
                mouseY = event.pos[1]
                col = mouseX // game_board.block_size   # определяем выбранную ячейку
                row = mouseY // game_board.block_size

                if game_board.spot_available(row, col):     # если ячейка свободна
                    if player == 1:                         # рисуем знак в зависимости от хода и переходим на след. ход
                        game_board.place_sign(row, col, 1)
                        player = 2
                    elif player == 2:
                        game_board.place_sign(row, col, 2)
                        player = 1

                    wins_table = game_board.win_check(win_length)   # получаем таблицу с выйгрышными ячейками
                    for row in range(len(wins_table)):              # цикл по всем ячейкам
                        for col in range(len(wins_table)):
                            if wins_table[row][col]:                # если ячейка не нулевая, рисуем линию
                                game_board.draw_win_line(col, row, wins_table[row][col], win_length, 10)
                                game_finished = True                # игра кончается
                                board_is_active = False             # доска отключается
                                if player == 2:             # проверка обратная, так как игрок уже был изменен
                                    end_message('Победа крестиков! Нажмите SPACE для новой игры',
                                                (33, 90, 136), font, screen)
                                elif player == 1:
                                    end_message('Победа ноликов! Нажмите SPACE для новой игры',
                                                (33, 90, 136), font, screen)

                    if not game_finished and game_board.is_full():
                        end_message('Ничья! Нажмите SPACE для новой игры',
                                    (33, 90, 136), font, screen)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_SPACE:             # при нажатии пробела создаем новую доску
                del game_board                          # удаляем старый объект (на всякий случай)
                game_board = Board(board_size, screen)
                player = 1
                board_is_active = True
                game_finished = False

    # Конец цикла
    pygame.display.update()         # обновление экрана (прорисовка)
    clock.tick(FPS)                 # задержка перед следующим кадром
