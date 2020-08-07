import sys
import os
import random
import copy

import pygame
from pygame.locals import *

import engine


# =========================================================================================
# Self-Explanatory functions

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


# Privides a delay between two lines of code.
def delay(j, d):
    i = 0
    while i < j:
        pygame.time.wait(d)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
              (event.type == KEYDOWN and event.key == K_ESCAPE):
                i = j + 1
                terminate()

# =========================================================================================


# =========================================================================================


# BOILERPLATE CODDE
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"
win_wt, win_ht = (9*16*4), (11*16*4)
fps_clock = pygame.time.Clock()
fps = 60
win = pygame.display.set_mode((win_wt, win_ht))
ico = load_img("ico.png")
pygame.display.set_icon(ico)


# FONTS
number_font = pygame.font.Font(os.path.join("assets", "font.ttf"), 20)
text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 50)
text_font_2 = pygame.font.Font(os.path.join("assets", "type.ttf"), 35)


# IMAGES
tick_img = load_img("tick.png")     # Tick Image
cross_img = load_img("cross.png")   # Cross Image
smiley = load_img("smiley.png")     # Smiley Image


# COLORS
BLACK = (0, 0, 0)
BGCOLOR = (78, 88, 74)

# =========================================================================================


# =========================================================================================

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


# Converts a 2-d array indexing to a 1-d array indexing.
def two_d(row, col):
    return (col) * 9 + (row + 1) - 1


# =========================================================================================

# Each cell that contains a number

class Cell(object):
    def __init__(self, value, x, y, row, col):
        # self.board = board
        self.value = value
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.rect = pygame.Rect(x, y, 54, 54)
        self.selected = False       # Checks if the cell is highlighted or not

    def __str__(self):
        return f"{self.value}, {self.row}, {self.col}"

    def draw(self, win):
        if self.value != 0:
            print_text(number_font, self.value, self.x + 17, self.y + 17)
        if self.selected:
            pygame.draw.rect(win, (200, 0, 0), [
                             45 + (self.col * 54) + 2, 109 + (self.row * 54) + 2, 54 - 3, 54 - 3], 3)
            pass

    # changes the text on the cell. Basicaly the same function as above, just with some fluff.
    def draw_change(self, win, green=True):

        pygame.draw.rect(win, BGCOLOR, [self.rect[0]+6, self.rect[1]+6,
                                             self.rect[2]-16, self.rect[3]-12], 0)

        print_text(number_font, self.value, self.x + 17, self.y + 17)

        if green:
            pygame.draw.rect(win, BLACK, [
                             45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 2)
            pass
        else:
            pygame.draw.rect(win, (150, 0, 0), [
                             45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 2)

        pass
# =========================================================================================


# =========================================================================================

# Board Class: The meat of the program, it draws the board, the buttons, gives them the functionality and other things.

class Board(object):

    def __init__(self, board):
        self.cols = 9
        self.rows = 9
        self.board = board
        self.backup = copy.deepcopy(board)            # Creates a copy of the original unsolved and unedited board.
        
        self.solve_box = pygame.Rect(45, 20, 54*2, 54)
        self.reset_box = pygame.Rect(45 + 54*2, 20, 54*2, 54)
        self.check_box = pygame.Rect(45 + 54*5, 20, 54*2, 54)
        
        self.nums = [Cell(self.board[i][j], j*54 + 27 + 19, i*54 + 45 + 27 + 38, i, j)  # This 1-d list contains the numbers, 
                                for j in range(self.cols) for i in range(self.rows)]    # each element is a Cell object.
        
        self.selected = [0, 0]                        # Keeps track of which number is currently selected.
        self.check = False

    def draw_box(self):
        
        # SOLVE 
        if self.solve_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.solve_box.x+6, self.solve_box.y+6,
                                    self.solve_box.width-16, self.solve_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.solve_box, 1)
        print_text(text_font_2, "Solve", self.solve_box.x +
                   22, self.solve_box.y + 5)

        # RESET
        if self.reset_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.reset_box.x+6, self.reset_box.y+6,
                                    self.reset_box.width-16, self.reset_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.reset_box, 1)
        print_text(text_font_2, "Reset", self.reset_box.x +
                   22, self.solve_box.y + 5)

        # CHECK
        if self.check_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, (123, 114, 67), [self.check_box.x+6, self.check_box.y+6,
                                    self.check_box.width-16, self.check_box.height-12], 0)

        pygame.draw.rect(win, BLACK, self.check_box, 1)
        print_text(text_font_2, "Check", self.check_box.x +
                   18, self.check_box.y + 5)
                   
    
    def draw(self, win):
        
        win.fill(BGCOLOR)
        draw_grid(win)
        self.draw_box()

        for cell in self.nums:
            if self.backup[cell.row][cell.col] != 0:
                pygame.draw.rect(
                    win, (24, 48, 75), [cell.rect[0]+6, cell.rect[1]+6, 
                    cell.rect[2]-16, cell.rect[3]-12])
            if cell.rect.collidepoint(pygame.mouse.get_pos()) and \
                (self.backup[cell.row][cell.col] == 0):
                pygame.draw.rect(win, (123, 114, 67), [cell.rect[0]+6, cell.rect[1] + 6, 
                                 cell.rect[2]-16, cell.rect[3]-12])
            
            cell.draw(win)

    # Syncs the grid and cells
    def cell_update(self):
        self.nums = [Cell(self.board[i][j], j*54 + 27 + 19, i*54 + 45 + 27 + 38, i, j) \
                    for j in range(self.cols) for i in range(self.rows)]

    # Resets the grid
    def reset(self):
        self.board = copy.deepcopy(self.backup)
        self.cell_update()

    # Solves the grid using backtracking algorithm
    def solve_(self):

        self.reset()
        
        def _recurse():
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
                    delay(2, 50)

                    if _recurse():
                        return True

                    self.board[row][col] = 0
                    self.nums[two_d(row, col)].value = num
                    self.nums[two_d(row, col)].draw_change(win, False)
                    pygame.display.update()
                    delay(2, 50)

            return False

        _recurse()

    # Selects a cell
    def select_cell(self, win, pos):
        for cell in self.nums:
            if cell.rect.collidepoint(pos):
                if self.backup[cell.row][cell.col] == 0:
                    self.selected = [cell.row, cell.col]
                    for box in self.nums:
                        box.selected = False
                    cell.selected = True
                    return self.selected


    # Keeps track of whether the check button is pressed or not.
    def check_press(self):

        if self.check:
            self.check = False
        else:
            self.check = True


    # Makes the buttons clickable 
    def select_box(self, pos):
        if self.solve_box.collidepoint(pos):
            self.solve_()
        elif self.reset_box.collidepoint(pos):
            self.reset()
        elif self.check_box.collidepoint(pos):
            self.check_press()


    # Eraser
    def clear(self):
        self.board[self.selected[0]][self.selected[1]] = 0
        self.cell_update()


    # Pencil.
    def edit(self, key):
        self.board[self.selected[0]][self.selected[1]] = key
        self.cell_update()

# =========================================================================================


def main():

    # Due to a lack of creativity, the name is misleading, this function 
    # creates the starting menu.
    def show_game_over_screen(minus):
        
        win.fill(BGCOLOR)
        
        draw_grid(win)
        
        title_img = load_img("title.png")
        win.blit(title_img, [45 + 54, 45 + 64 + (2*54)])
        _font = pygame.font.Font(os.path.join("assets", "font.ttf"), 64)
        print_text(_font, "SUDOKU", 99, 108 + 90 + 45)
        
        _text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 54)
        item = _text_font.render("press space to start", True, BLACK)
        item_rect = item.get_rect()
        item_rect.topleft = (win_wt//2 - item_rect.width//2, 45 + 64 + (8*54) - 10)
        pygame.draw.rect(win, BGCOLOR, [item_rect.x - 15, item_rect.y + 11, 
                                            item_rect.width + 15 + 15, item_rect.height - 10])
        win.blit(item, item_rect)
        
        pygame.draw.rect(win, BGCOLOR, [(45 + 54*3 + 2), (99 + (4*54) + 11), (54*3 - 2), (54*4 - 1)])

        box_font = pygame.font.Font(os.path.join("assets", "font.ttf"), 24)
        
        easy = box_font.render("Easy", True, BLACK)
        easy_rect = easy.get_rect()
        easy_rect.topleft = ((45 + 54*3 + 35), 45 + 64 + (5*54) - 10)
        win.blit(easy, easy_rect)
             
        medium = box_font.render("Medium", True, BLACK)
        medium_rect = medium.get_rect()
        medium_rect.topleft = ((45 + 54*3 + 12), 45 + 64 + (6*54) - 10)
        win.blit(medium, medium_rect)
               
        hard = box_font.render("Hard", True, BLACK)
        hard_rect = hard.get_rect()
        hard_rect.topleft = ((45 + 54*3 + 35), 45 + 64 + (7*54) - 10)
        win.blit(hard, hard_rect)

        def draw_easy():
            pygame.draw.rect(win, BLACK, [easy_rect.x - 5, easy_rect.y - 5,
                                          easy_rect.width + 10, easy_rect.height + 10], 1)
            pygame.draw.rect(win, BGCOLOR, [medium_rect.x - 5, medium_rect.y - 5,
                                          medium_rect.width + 10, medium_rect.height + 10], 1)
            pygame.draw.rect(win, BGCOLOR, [hard_rect.x - 5, hard_rect.y - 5,
                                          hard_rect.width + 10, hard_rect.height + 10], 1)
            pygame.display.update()

        def draw_medium():
            pygame.draw.rect(win, BGCOLOR, [easy_rect.x - 5, easy_rect.y - 5,
                                          easy_rect.width + 10, easy_rect.height + 10], 1)
            pygame.draw.rect(win, BLACK, [medium_rect.x - 5, medium_rect.y - 5,
                                          medium_rect.width + 10, medium_rect.height + 10], 1)
            pygame.draw.rect(win, BGCOLOR, [hard_rect.x - 5, hard_rect.y - 5,
                                          hard_rect.width + 10, hard_rect.height + 10], 1)
            pygame.display.update()

        def draw_hard():
            pygame.draw.rect(win, BGCOLOR, [easy_rect.x - 5, easy_rect.y - 5,
                                          easy_rect.width + 10, easy_rect.height + 10], 1)
            pygame.draw.rect(win, BGCOLOR, [medium_rect.x - 5, medium_rect.y - 5,
                                          medium_rect.width + 10, medium_rect.height + 10], 1)
            pygame.draw.rect(win, BLACK, [hard_rect.x - 5, hard_rect.y - 5,
                                          hard_rect.width + 10, hard_rect.height + 10], 1)
            pygame.display.update()
        
        pygame.display.update()    

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if (event.type == KEYDOWN):
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_SPACE:
                        return minus

                # Checks for mouse button press
                if event.type == MOUSEBUTTONDOWN:
                    # Checks for left mouse button press
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if easy_rect.collidepoint(pos):
                            minus = random.randint(20, 30)
                            draw_easy()
                        if medium_rect.collidepoint(pos):
                            minus = random.randint(30, 40)
                            draw_medium()
                        if hard_rect.collidepoint(pos):
                            minus = random.randint(40, 50)
                            draw_hard()
                        

    def animate(grid):
        _grid = Board(grid)

        win.fill(BGCOLOR)
        draw_grid(win)
        _grid.draw_box()

        # Animates the board display
        for cell in _grid.nums:
            if _grid.backup[cell.row][cell.col] != 0:
                pygame.draw.rect(win, (24, 48, 75), [cell.rect[0]+6, cell.rect[1]+6, 
                                                    cell.rect[2]-16, cell.rect[3]-12], 0)

            cell.draw(win)
            pygame.display.update()
            delay(3, 4)

        return
    

    def run_game(minus):

        _, grid = engine.generate_grid(minus)
        # engine.print_grid(grid)
        # engine.print_grid(_)

        board = Board(grid)
        animate(grid)
        key = None                    # Keeps track of which number key is pressed

        while True:
            board.draw(win)

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return

                # Checks for number keys being pressed
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

            # Checks if the board is filled, if yes sets board checking to true.
            if engine.find_empty_loc(board.board) == None:
                board.check = True
                

            # Checks if the player board is corrent, and does prints appropriate image.
            if board.check:
                check_against = copy.deepcopy(board.backup)
                engine.solve_grid(check_against)
                if board.board == check_against:
                    win.blit(smiley, [
                        win_wt//2 - smiley.get_width()//2, 
                        win_ht//2 - smiley.get_height()//2])
                    pygame.display.update()
                    delay(5, 200)
                    return
                if (engine.find_empty_loc(board.board) != None):
                    c = True
                    for i in range(9):
                        for j in range(9):
                            if (board.board[i][j] != 0) and (board.board[i][j] != board.backup[i][j]):
                                if (board.board[i][j] != check_against[i][j]):
                                    c = False
                    
                    if (not c):
                        win.blit(cross_img, [
                            win_wt//2 - cross_img.get_width()//2, 
                            win_ht//2 - cross_img.get_height()//2])
                    else:
                        win.blit(tick_img, [
                            win_wt//2 - tick_img.get_width()//2,
                            win_ht//2 - tick_img.get_height()//2])
                        board.check = False
                    pygame.display.update()                                    
                    delay(5, 150)
                    board.check = False

            if board.selected and key != None:
                board.edit(key)
                key = None

            
            fps_clock.tick(fps)
            pygame.display.update()

    while True:
        minus = 25
        minus = show_game_over_screen(minus)
        run_game(minus)


if __name__ == "__main__":
    main()
    pygame.quit()
