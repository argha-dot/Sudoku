import sys
import os
import copy
import pprint
import pygame
from pygame.locals import *
import engine


pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"


def terminate():
    pygame.quit()
    sys.exit()


def print_text(font, text, x, y):
    win.blit(font.render(str(text), True, (0, 0, 0)), (x, y))


def load_img(name):
    fullname = os.path.join("assets", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print("Can't load image: ", name)
        raise SystemExit(e)
    image = image.convert_alpha()
    return image


def delay(j, d):
    i = 0
    while i < j:
        pygame.time.wait(d)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                i = j + 1
                terminate()


win_wt, win_ht = (9*16*4), (11*16*4)
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))
ico = load_img("ico.png")
pygame.display.set_icon(ico)

number_font = pygame.font.Font(os.path.join("assets", "font.ttf"), 20)
text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 50)
text_font_2 = pygame.font.Font(os.path.join("assets", "type.ttf"), 35)
tick_img = pygame.image.load(os.path.join(
        "assets", "tick.png")).convert_alpha()
cross_img = pygame.image.load(os.path.join(
        "assets", "cross.png")).convert_alpha()

BLACK = (0, 0, 0)
GREY = (100, 100, 100)


def draw_grid(win):
    for i in range(0, 10):
        if (i % 3) == 0:
            # horizontal lines
            pygame.draw.line(win, BLACK, (45, 64 + 45 + (i * 54)),
                                (win_wt - 45, 64 + 45 + (i * 54)), 2)

            # vertical lines
            pygame.draw.line(win, BLACK, (45 + (i * 54),
                                            64 + 45), (45 + (i * 54), win_ht - 64 - 45), 2)
        else:
            # horizontal lines
            pygame.draw.line(win, BLACK, (45, 64 + 45 + (i * 54)),
                                (win_wt - 45, 64 + 45 + (i * 54)), 1)

            # vertical lines
            pygame.draw.line(win, BLACK, (45 + (i * 54),
                                            64 + 45), (45 + (i * 54), win_ht - 64 - 45))
    pass


def two_d(row, col):
    return (col) * 9 + (row + 1) - 1


class Cell(object):
    def __init__(self, value, x, y, row, col):
        # self.board = board
        self.value = value
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.rect = pygame.Rect(x, y, 54, 54)
        self.selected = False

    def __str__(self):
        return f"{self.value}, {self.row}, {self.col}"

    def draw(self, win):
        if self.value != 0:
            print_text(number_font, self.value, self.x + 17, self.y + 17)
        if self.selected:
            pygame.draw.rect(win, (200, 0, 0), [
                             45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 3)
            pass

    def draw_change(self, win, green=True):

        pygame.draw.rect(win, [78, 88, 74], [self.rect[0]+6, self.rect[1]+6,
                                             self.rect[2]-16, self.rect[3]-12], 0)

        print_text(number_font, self.value, self.x + 17, self.y + 17)

        if green:
            pygame.draw.rect(win, BLACK, [
                             45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 3)
        else:
            pygame.draw.rect(win, (150, 0, 0), [
                             45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 3)

        pass


class Board(object):

    # FIXME Fix the check thingy

    def __init__(self, board):
        self.cols = 9
        self.rows = 9
        self.board = board
        self.backup = copy.deepcopy(board)
        self.solve_box = pygame.Rect(45, 20, 54*2, 54)
        self.reset_box = pygame.Rect(45 + 54*2, 20, 54*2, 54)
        self.check_box = pygame.Rect(45 + 54*5, 20, 54*2, 54)
        self.nums = [Cell(self.board[i][j], j*54 +
                          27 + 19, i*54 + 45 + 27 + 38, i, j) for j in range(self.cols) for i in range(self.rows)]
        self.selected = [0, 0]
        self.check = False
        # self.solved = False

    def draw_box(self):
        if self.solve_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.solve_box.x+6, self.solve_box.y+6,
                                                   self.solve_box.width-16, self.solve_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.solve_box, 1)
        print_text(text_font_2, "Solve", self.solve_box.x +
                   22, self.solve_box.y + 5)

        if self.reset_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.reset_box.x+6, self.reset_box.y+6,
                                                   self.reset_box.width-16, self.reset_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.reset_box, 1)
        print_text(text_font_2, "Reset", self.reset_box.x +
                   22, self.solve_box.y + 5)

        if self.check_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.check_box.x+6, self.check_box.y+6,
                                                   self.check_box.width-16, self.check_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.check_box, 1)
        print_text(text_font_2, "Check", self.check_box.x +
                   18, self.check_box.y + 5)
        pass
    
    def draw(self, win):
        
        win.fill([78, 88, 74])

        draw_grid(win)

        self.draw_box()

        for cell in self.nums:
            if self.backup[cell.row][cell.col] != 0:
                pygame.draw.rect(
                    win, (24, 48, 75), [cell.rect[0]+6, cell.rect[1]+6, cell.rect[2]-16, cell.rect[3]-12], 0)
            if cell.rect.collidepoint(pygame.mouse.get_pos()) & (self.backup[cell.row][cell.col] == 0):
                pygame.draw.rect(win, (123, 114, 67), [
                                 cell.rect[0]+6, cell.rect[1]+6, cell.rect[2]-16, cell.rect[3]-12], 0)
            cell.draw(win)

    def cell_update(self):
        self.nums = [Cell(self.board[i][j], j*54 +
                          27 + 19, i*54 + 45 + 27 + 38, i, j) for j in range(self.cols) for i in range(self.rows)]

    def reset(self):
        self.board = self.backup[:]
        self.cell_update()

    def _solve(self):
        self.reset()
        engine.solve_grid(self.board)
        self.cell_update()

    def solve_(self):
        self.reset()
        find = engine.find_empty_loc(self.board)
        if find == None:
            return True
        else:
            row, col = find[0], find[1]

        for num in range(1, 10):
            if engine.isValid(self.board, row, col, num):
                self.board[row][col] = num
                self.nums[two_d(row, col)].value = num
                self.nums[two_d(row, col)].draw_change(win)
                pygame.display.update()
                delay(2, 75)

                if self.solve_():
                    return True

                self.board[row][col] = 0
                self.nums[two_d(row, col)].value = num
                self.nums[two_d(row, col)].draw_change(win, False)
                pygame.display.update()
                delay(2, 75)

        return False

    def select_cell(self, win, pos):
        for cell in self.nums:
            if cell.rect.collidepoint(pos):
                if self.backup[cell.row][cell.col] == 0:
                    self.selected = [cell.row, cell.col]
                    for box in self.nums:
                        box.selected = False
                    cell.selected = True
                    return self.selected

    def check_press(self):

        if self.check:
            self.check = False
        else:
            self.check = True

    def select_box(self, pos):
        if self.solve_box.collidepoint(pos):
            # self._solve()
            self.solve_()
        elif self.reset_box.collidepoint(pos):
            self.reset()
        elif self.check_box.collidepoint(pos):
            self.check_press()

    def clear(self):
        self.board[self.selected[0]][self.selected[1]] = 0
        self.cell_update()

    def edit(self, key):
        self.board[self.selected[0]][self.selected[1]] = key
        self.cell_update()


def main():

    def show_game_over_screen():
        
        win.fill([78, 88, 74])
        
        draw_grid(win)
        
        title_img = load_img("title.png")
        win.blit(title_img, [45 + 54, 45 + 64 + (2*54)])
        _font = pygame.font.Font(os.path.join("assets", "font.ttf"), 64)
        print_text(_font, "SUDOKU", 99, 108 + 90 + 45)
        
        _text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 54)
        item = _text_font.render("press space to start", True, BLACK)
        item_rect = item.get_rect()
        item_rect.topleft = (win_wt//2 - item_rect.width//2, 45 + 64 + (8*54))
        pygame.draw.rect(win, [78, 88, 74], [
                         item_rect.x - 15, item_rect.y + 1, item_rect.width + 15 + 15, item_rect.height])
        win.blit(item, item_rect)
        
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if (event.type == KEYDOWN):
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_SPACE:
                        return


    def animate(grid):
        _grid = Board(grid)

        win.fill([78, 88, 74])
        draw_grid(win)
        _grid.draw_box()

        for cell in _grid.nums:
            if _grid.backup[cell.row][cell.col] != 0:
                pygame.draw.rect(
                    win, (24, 48, 75), [cell.rect[0]+6, cell.rect[1]+6, cell.rect[2]-16, cell.rect[3]-12], 0)

            cell.draw(win)
            pygame.display.update()
            delay(3, 4)

        return
    

    def run_game():
        
        minus = 25
        _, grid = engine.generate_grid(minus)
        # engine.print_grid(grid)
        # engine.print_grid(_)
        # print("")

        board = Board(grid)
        animate(grid)
        key = None

        while True:
            board.draw(win)

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return

                if event.type == pygame.KEYDOWN:
                    if (event.key == K_1) or (event.key == K_KP1):
                        key = 1
                    if (event.key == K_2) or (event.key == K_KP2):
                        key = 2
                    if (event.key == K_3) or (event.key == K_KP3):
                        key = 3
                    if (event.key == K_4) or (event.key == K_KP4):
                        key = 4
                    if (event.key == K_5) or (event.key == K_KP5):
                        key = 5
                    if (event.key == K_6) or (event.key == K_KP6):
                        key = 6
                    if (event.key == K_7) or (event.key == K_KP7):
                        key = 7
                    if (event.key == K_8) or (event.key == K_KP8):
                        key = 8
                    if (event.key == K_9) or (event.key == K_KP9):
                        key = 9
                    if (event.key == K_DELETE) or (event.key == K_BACKSPACE):
                        board.clear()

                if (event.type == MOUSEBUTTONDOWN):
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        click = board.select_cell(win, pos)
                        if click:
                            key = None
                        else:
                            board.select_box(pos)

            if engine.find_empty_loc(board.board) == None:
                board.check = True
                

            if board.check:
                check_against = copy.deepcopy(board.backup)
                engine.solve_grid(check_against)
                if board.board == check_against:
                    win.blit(tick_img, [
                        win_wt//2 - tick_img.get_width()//2, win_ht//2 - tick_img.get_height()//2])
                    pygame.display.update()
                    delay(5, 150)
                    return
                else:
                    win.blit(cross_img, [
                        win_wt//2 - tick_img.get_width()//2, win_ht//2 - cross_img.get_height()//2])
                    pygame.display.update()
                    delay(5, 150)
                    board.check = False

            if board.selected and key != None:
                board.edit(key)
                key = None

            fps_clock.tick(60)
            pygame.display.update()

    while True:
        show_game_over_screen()
        run_game()


if __name__ == "__main__":
    main()
    pygame.quit()
