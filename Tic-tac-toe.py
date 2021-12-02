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


def exit_button_click():
    pygame.quit()
    sys.exit(0)

def restart():
    global game_board, player, board_is_active, game_finished, board_size, win_length, max_board_size, min_board_size, min_win_length
    del game_board  # удаляем старый объект (на всякий случай)
    if len(text_box1.text) and min_board_size <= int(text_box1.text) <= max_board_size:
        board_size = int(text_box1.text)
        label1.text = f'Размер поля:              {board_size} x {board_size}'
    if len(text_box2.text) and int(text_box2.text) >= min_win_length:
        win_length = int(text_box2.text)
        label2.text = f'Условие победы:     {win_length} в ряд'
    game_board = Board(board_size, board_surface)
    player = 1
    board_is_active = True
    game_finished = False


# Класс поля ввода текста
class TextBox:
    def __init__(self, pos, size,
                 color_active='red', color_inactive='lightcyan',
                 text='', font='None', font_size=24):
        self.x, self.y = pos
        self.width, self.height = size
        self.box_surface = pygame.Surface(size)
        self.rect = self.box_surface.get_rect(bottomleft=(self.x, self.y))
        self.color_active, self.color_inactive = color_active, color_inactive
        self.color = self.color_inactive
        self.is_active = False
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.draw()

    def draw(self):
        # заполнение поверхности цветом, прорисовка рамки, нанесение текста и нанесение самого поля
        self.box_surface.fill(self.color)
        pygame.draw.rect(self.box_surface, black, self.box_surface.get_rect() , width=1)
        self.box_surface.blit(self.font.render(self.text, True, black), (3,2))
        screen.blit(self.box_surface, self.rect)

    # метод обработки нажатия мыши (для активации поля ввода)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # если игрок кликнул по полю ввода
            if self.rect.collidepoint(event.pos):
                 # сделать поле активным
                self.is_active = True
            else:   # иначе, сделать неактивным
                self.is_active = False
        # нажатие клавишь при выбранном поле ввода
        elif event.type == pygame.KEYDOWN:
            if self.is_active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                    self.text += event.unicode


    def update(self):
        if self.is_active:
            self.color = self.color_active
        else:
            self.color = self.color_inactive
        self.draw()



# Класс надписи
class Label:
    def __init__(self, x, y, text, surface, font='None', font_size=20, color='black', x_centered=False):
        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.color = color
        self.surface = surface
        self.x = x
        self.y = y
        self.x_centered = x_centered

    def draw(self): # возможно бессмысленна, как и этот класс в целом
        text_surface = self.font.render(self.text, True, self.color)
        if self.x_centered:
            self.x = self.surface.get_rect().width / 2 - text_surface.get_rect().width / 2
        text_rect = text_surface.get_rect(bottomleft=(self.x, self.y))
        self.surface.blit(text_surface, text_rect)


# Класс кнопки
class Button:
    def __init__(self, pos, size, text, font='Arial', font_size=20,
                 background_color='white', text_color='black',
                 clicked_bg_color='black', clicked_text_color='white',
                 hover_bg_color='gray', hover_text_color='black'):
        self.x, self.y = pos                                # устанавливаем позицию и размеры
        self.width, self.height = size
        self.font = pygame.font.SysFont(font, font_size)    # создаем объект шрифта
        self.text = text
        self.background_color = self.normal_bg_color = background_color
        self.text_color = self.normal_text_color = text_color
        self.hovered_bg_color = hover_bg_color
        self.hovered_text_color = hover_text_color
        self.clicked_bg_color = clicked_bg_color
        self.clicked_text_color = clicked_text_color
        self.surface = pygame.Surface((self.width, self.height))    # создаем поверхность кнопки
        self.rect = self.surface.get_rect(topleft=pos)             # создаем прямоугольник по размерам и месту кнопки
        self.state = 'none'
        self.clicked = False

    # прорисовка кнопки на основном экране
    def draw(self):
        self.surface.fill(self.background_color)                    # заполняем поверхность кнопки цветом
        text_surface = self.font.render(self.text, True, self.text_color)   # создаем надпись с ее поверхностью
        # получаем прямоугольник с центром в центре кнопки
        text_rect = text_surface.get_rect(center=(self.surface.get_rect().width / 2, self.surface.get_rect().height / 2))
        self.surface.blit(text_surface, text_rect)      # прорисовываем надпись на поверхности кнопки
        screen.blit(self.surface, (self.x, self.y))     # прорисовываем кнопку на основном экране

    # функция определяющая состояние кнопки (обычное, наведение, клик)
    def get_state(self):
        mouse_pos = pygame.mouse.get_pos()      # получаем позицию мыши
        if self.rect.collidepoint(mouse_pos):   # если мышь находится в прямоугольнике кнопки
            if pygame.mouse.get_pressed()[0] == 1:     # если при этом нажата ЛКМ
                return 'clicked'                # состояние - нажатая
            else:
                return 'hovered'                # находится в прямоуг., но нет нажатия, то состояние - наведенная
        else:
            return 'none'                       # не находится в прямоуг. - состояние никакое

    # функция обновляющая вид кнопки в зависимости от состояния и возвращающая bool, указывающий стоит ли делать
    # соответствующие кнопке действие
    def update(self):
        action = False                      # изначально действия делать не нужно

        if self.get_state() == 'hovered':
            self.background_color = self.hovered_bg_color
            self.text_color = self.hovered_text_color
            self.clicked = False
        elif self.get_state() == 'clicked':
            self.background_color = self.clicked_bg_color
            self.text_color = self.clicked_text_color
            if not self.clicked:            # действие совершается только тогда, когда кнопка кликнута и не зажата,
                self.clicked = True         # то есть прошлое состояние не было кликом. Действие выполняется один
                action = True               # раз сразу же по нажатию
        else:
            self.background_color = self.normal_bg_color
            self.text_color = self.normal_text_color
            self.clicked = False

        self.draw()                         # рисуем кнопку с заданным дизайном
        return action                       # возвращаем указание к действию (или бездействию)



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
        pygame.draw.rect(self.surface, light_cyan, self.surface.get_rect(), 5)  # рамка
        for i in range(self.size - 1):                                          # цикл прорисовки линий
            # вертикальная линия
            x1 = x2 = self.block_size * (i + 1)
            y1 = 0
            y2 = self.width
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 5)
            # горизонтальная линия
            x1 = 0
            y1 = y2 = self.block_size * (i + 1)
            x2 = self.width
            pygame.draw.line(self.surface, light_cyan, (x1, y1), (x2, y2), 5)

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
blue_2 = (33, 90, 136)

win_width = 1100                    # ширина окна
win_height = 800                   # высота окна
padding = 100
board_height = board_width = win_height - padding * 2    # высота поля
board_position_x = win_width - board_width - padding            # положение поверхности игрового поля в основном экране
board_position_y = padding

FPS = 100                           # количество кадров, для определения задержки
font = pygame.font.SysFont(None, 30, bold=True)     # Определение объекта-шрифта

screen = pygame.display.set_mode((win_width, win_height))     # инициализация основного окна
icon = pygame.image.load("icon.bmp")
pygame.display.set_icon(icon)                                 # иконка 32x32
screen.fill(blue_2)
board_surface = pygame.Surface((board_width, board_height))    # создание поверхности для игрового поля
pygame.display.set_caption('Крестики-нолики')                                   # надпись на окне

clock = pygame.time.Clock()         # инициализация объекта часов, используемого для задержки

# Предшествующие игре действия
board_size = 3
win_length = 3
max_board_size = 25
min_board_size = 2
min_win_length = 2
game_board = Board(board_size, board_surface)       # создание объекта-поля для игры

player = 1                          # ходит первый игрок
board_is_active = True              # доска активирована
game_finished = False               # игра не закончена

# элементы интерфейса
# панели (плоскости)
panel1 = pygame.Surface((300, 110))
panel1_rect = panel1.get_rect()
panel1.fill(blue_1)
panel2 = pygame.Surface((300, 250))
panel2_rect = panel2.get_rect()
panel2.fill(blue_1)

# кнопки
restart_button = Button((padding/2, 575), (300, 50), 'Начать заново', font_size=30, background_color=light_cyan, hover_bg_color='purple')             # кнопка рестарта
exit_button = Button((padding/2, 650), (300, 50), 'Выход',font_size=30, hover_bg_color=red, background_color=light_cyan)     # кнопка выход

# надписи
static_label1 = Label(0, 30, 'Текущие правила', panel1, font_size=30, x_centered=True)
static_label2 = Label(0, 30, 'Новые правила', panel2, font_size=30, x_centered=True)
static_label3  = Label(5, 65, 'Размер поля: ', panel2, font_size=24)
static_label4  = Label(5, 95, 'Условие победы: ', panel2, font_size=24)
static_label5 = Label(5, 135, f'Ограничения:', panel2, font_size=24,
                      color=light_cyan)
static_label6 = Label(5, 155, f'Размер поля от {min_board_size} до {max_board_size}', panel2, font_size=24,
                      color=light_cyan)
static_label7  = Label(5, 175, f'Условие победы больше {min_win_length - 1}', panel2, font_size=24, color=light_cyan)
static_label8  = Label(5, 220, 'Новые правила применяются после', panel2, font_size=24, color=light_cyan)
static_label9  = Label(5, 240, 'перезапуска', panel2, font_size=24, color=light_cyan, x_centered=True)


label1 = Label(5, 65, f'Размер поля:              {board_size} x {board_size}', panel1, font_size=24)
label2 = Label(5, 95, f'Условие победы:     {win_length} в ряд', panel1, font_size=24)
label3 = Label(570, 70, 'Ход крестиков', screen, font='Consolas', font_size=35)
labels = (label1, label2, label3, static_label1, static_label2, static_label3, static_label4, static_label5, static_label6,
          static_label7, static_label8, static_label9)

# поля ввода текста
text_box1 = TextBox((220, 315), (100, 17))
text_box2 = TextBox((220, 345), (100, 17))
text_boxes = (text_box1, text_box2)

# основной цикл игры
while True:
    screen.fill(blue_2)
    # Цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # выход из программы
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:    # клик мышью
            if event.button == 1:                   # если ЛКМ
                mouseX = event.pos[0]  # получаем координаты клика
                mouseY = event.pos[1]

                if board_is_active and board_surface.get_rect(left=board_position_x, top=board_position_y)\
                        .collidepoint(event.pos):   # проверяем активность поля и производится ли клик внутри него

                    mouseX -= board_position_x    # получаем координаты относительно игровой поверхности
                    mouseY -= board_position_y

                    col = mouseX // game_board.block_size   # определяем выбранную ячейку
                    row = mouseY // game_board.block_size

                    if game_board.spot_available(row, col):     # если ячейка свободна
                        if player == 1:                         # рисуем знак в зависимости от хода и переходим на с.х.
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
                                        end_message('Победа крестиков!',
                                                    blue_2, font, board_surface)
                                    elif player == 1:
                                        end_message('Победа ноликов!',
                                                    blue_2, font, board_surface)

                        if not game_finished and game_board.is_full():
                            end_message('Ничья!',
                                        blue_2, font, board_surface)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_SPACE:             # при нажатии пробела создаем новую доску
                restart()

        # обрабатываем поля ввода текста
        for box in text_boxes:
            box.handle_event(event)

    if player == 1:
        label3.text = "Ход крестиков"
    else:
        label3.text = "Ход ноликов"

    panel1.fill(blue_1)
    panel2.fill(blue_1)
    for label in labels:
        label.draw()
    screen.blit(panel1, (padding / 2, padding))
    screen.blit(panel2, (padding / 2, 250))

    # обновление состояний кнопок
    if exit_button.update():
        exit_button_click()
    if restart_button.update():
        restart()
    for box in text_boxes:
        box.update()

    # Конец цикла
    screen.blit(board_surface, (board_position_x, board_position_y))
    pygame.display.update()         # обновление экрана (прорисовка)
    clock.tick(FPS)                 # задержка перед следующим кадром
