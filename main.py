import sys, os, copy
import pygame
from pygame.locals import *
import engine

pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"

win_wt, win_ht = (9*16*4), (11*16*4)
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))
number_font = pygame.font.Font(os.path.join("assets", "font.ttf"), 20)
text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 50)
text_font_2 = pygame.font.Font(os.path.join("assets", "type.ttf"), 35)

BLACK = (0, 0, 0)
GREY = (100, 100, 100)


def terminate():
    pygame.quit()
    sys.exit()


def print_text(font, text, x, y):
    win.blit(font.render(str(text), True, (0, 0, 0)), (x, y))
    pass


def delay(j, d):
    i = 0
    while i < j:
        pygame.time.delay(d)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 201
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    i = 201
                    terminate()


def load_img(name):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print("Can't load image: ", name)
        raise SystemExit(e)
    image = image.convert_alpha()
    return image


def one_d(number, divisor):
    return [number // divisor, number % divisor]
    pass


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
        # return f"value: {self.value}\nrow: {self.row}\ncol: {self.col}"
        return f"{self.value}"

    def draw(self, win):            
        if self.value != 0:
            print_text(number_font, self.value, self.x + 17, self.y + 17)
        if self.selected:
            pygame.draw.rect(win, (200, 0, 0), [45 + (self.col * 54), 109 + (self.row * 54), 54, 54], 3)


class Board(object):

    def __init__(self, board):
        self.cols = 9
        self.rows = 9
        self.board = board
        self.backup = copy.deepcopy(board)
        self.solve_box = pygame.Rect(45, 20, 54*2, 54)
        self.reset_box = pygame.Rect(45 + 54*2 + 27, 20, 54*2, 54)
        self.rough_box = pygame.Rect(45 + 54*5, 20, 54*2, 54)
        self.nums = [Cell(self.board[i][j], j*54 +
                          27 + 19, i*54 + 45 + 27 + 38, i, j) for j in range(self.cols) for i in range(self.rows)]
        self.selected = [0, 0]

    def draw(self, win):

        win.fill([74, 144, 226])
        
        # Grids
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
        

        pygame.draw.rect(win, BLACK, self.solve_box, 1)
        print_text(text_font_2, "Solve", self.solve_box.x + 22, self.solve_box.y + 5)

        pygame.draw.rect(win, BLACK, self.reset_box, 1)
        print_text(text_font_2, "Reset", self.reset_box.x + 22, self.solve_box.y + 5)

        pygame.draw.rect(win, BLACK, self.rough_box, 1)
        print_text(text_font_2, "Rough", self.rough_box.x +
                   5, self.solve_box.y + 3)


        for cell in self.nums:
            if self.backup[cell.row][cell.col] != 0:
                pygame.draw.rect(
                    win, (24, 48, 75), [cell.rect[0]+6, cell.rect[1]+6, cell.rect[2]-16, cell.rect[3]-12], 0)
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(win, GREY, [cell.rect[0]+6, cell.rect[1]+6, cell.rect[2]-16, cell.rect[3]-12], 0)
            cell.draw(win)


    def cell_update(self):
        self.nums = [Cell(self.board[i][j], j*54 +
                          27 + 19, i*54 + 45 + 27 + 38, i, j) for j in range(self.cols) for i in range(self.rows)]
        pass


    def reset(self):
        self.board = copy.deepcopy(self.backup)
        self.cell_update()

    def _solve(self):
        self.reset()
        engine.solve_grid(self.board)
        self.cell_update()
        
        pass

    def select_cell(self, win, pos):
        for cell in self.nums:
            if cell.rect.collidepoint(pos):
                if self.backup[cell.row][cell.col] == 0:
                    self.selected = [cell.row, cell.col]
                    for box in self.nums:
                        box.selected = False
                    cell.selected = True
                    return self.selected


    def select_box(self, pos):
        if self.solve_box.collidepoint(pos):
            self._solve()
        elif self.reset_box.collidepoint(pos):
            self.reset()
        

    def clear(self):
        self.board[self.selected[0]][self.selected[1]] = 0
        self.cell_update()
        pass


    def edit(self, key):
        self.board[self.selected[0]][self.selected[1]] = key
        self.cell_update()
        pass


def main():

    _, grid = engine.generate_grid(45)

    # engine.print_grid(grid)
    engine.print_grid(_)

    def run_game():

        board = Board(grid)
        key = None
        
        while True:
            # out_events()
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate() 
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    terminate()

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
                            # print(board.selected) 
                            # print(board.board[click[0]][click[1]]) 
                        else:
                            board.select_box(pos)
                            pass

                        
            if board.selected and key != None:
                board.edit(key)
                key = None
                pass


            board.draw(win)     
            
            if board.board == _:
                # pygame.draw.rect(win, BLACK, [win_wt//2 - 160, win_ht//2 - 80, 320, 160], 5)
                pass
              
            
            dt = fps_clock.tick(fps) / 1000
            dt *= 60

            pygame.display.update()

    while True:
        run_game()
        pass


if __name__ == "__main__":
    main()
    # print(one_d(9, 9))
    pygame.quit()
