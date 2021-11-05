import pygame
import sys


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

    # Прорисовка поля
    def draw_board(self):
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

        # Поиск вертикальных побед
        for col in range(self.size):                    # по всем столбцам
            for row in range(self.size - length + 1):   # проверяем каждую ячейку на победу "внизу"
                if self.table[col][row] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[col][row]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек внизу
                        if x == self.table[col][row+i]:     # если ячейки снизу совпадают
                            vertical_win = True        # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            vertical_win = False
                            break
                    if vertical_win:                    # если зафиксирована победа
                        return col, row, 'vertical'     # вернуть ячейку и указание на победу

        # Поиск горизонтальных побед
        for row in range(self.size):                    # по всем строкам
            for col in range(self.size - length + 1):   # проверяем каждую ячейку на победу "справа"
                if self.table[col][row] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[col][row]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек справа
                        if x == self.table[col+i][row]:     # если ячейки справа совпадают
                            horizontal_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            horizontal_win = False
                            break
                    if horizontal_win:
                        return col, row, 'horizontal'

        # Поиск победы на диагонали в правую сторону
        for row in range(self.size - length + 1):
            for col in range(self.size - length + 1):   # проверяем каждую ячейку на диагональ справа-снизу
                if self.table[col][row] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[col][row]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек справа-снизу
                        if x == self.table[col+i][row+i]:     # если ячейки справа-снизу совпадают
                            right_diag_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            right_diag_win = False
                            break
                    if right_diag_win:
                        return col, row, 'r-diagonal'

        # Поиск победы на диагонали в левую сторону
        for row in range(self.size - length + 1):
            for col in range(length - 1, self.size):   # проверяем каждую ячейку на диагональ слева-снизу
                if self.table[col][row] == 0:           # если в ячейке 0, пропускаем её
                    pass
                else:
                    x = self.table[col][row]            # значение ячейки
                    for i in range(1, length):        # цикл на проверку length ячеек слева-снизу
                        if x == self.table[col-i][row+i]:     # если ячейки слева-снизу совпадают
                            left_diag_win = True       # устанавливаем победу, возможно временно
                        else:                           # иначе, убираем победу и выходим из цикла
                            left_diag_win = False
                            break
                    if left_diag_win:
                        return col, row, 'l-diagonal'

        return 0


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

win_width = 700                    # ширина окна
win_height = 700                   # высота окна
FPS = 50                           # количество кадров, для определения задержки

screen = pygame.display.set_mode((win_width, win_height))     # инициализация основного окна
pygame.display.set_caption('Крестики-нолики')                                   # надпись на окне

clock = pygame.time.Clock()         # инициализация объекта часов, используемого для задержки

# Предшествующие игре действия
screen.fill(blue_1)                 # заполнение экрана цветом
game_board = Board(10, screen)       # создание объекта-поля для игры

player = 1                          # ходит первый игрок

# основной цикл игры
while True:
    # Цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # выход из программы
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:    # клик ЛКМ по окну
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
            print(game_board.win_check(4))
    # Конец цикла
    pygame.display.update()         # обновление экрана (прорисовка)
    clock.tick(FPS)                 # задержка перед следующим кадром
