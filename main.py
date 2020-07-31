import sys, os
import pygame
from pygame.locals import *
import engine

pygame.init()

win_wt, win_ht = (9*16*4), (11*16*4)
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))
number_font = pygame.font.Font(os.path.join("assets", "font.ttf"), 20)
text_font = pygame.font.Font(os.path.join("assets", "type.ttf"), 50)
text_font_2 = pygame.font.Font(os.path.join("assets", "type.ttf"), 35)


def terminate():
    pygame.quit()
    sys.exit()


def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


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


class Board(object):
    def __init__(self, board):
        self.board = board
        self.solve_box = pygame.Rect(45, 20, 54*2, 54)
        self.erase_box = pygame.Rect(45 + 54*2 + 27, 20, 54*2, 54)
        self.rough_box = pygame.Rect(45 + 54*5, 20, 54*2, 54)

    def draw(self, win):

        win.fill([74, 144, 226])
        
        # Grids
        for i in range(0, 10):
            if (i % 3) == 0:
                # horizontal lines
                pygame.draw.line(win, (0, 0, 0), (45, 64 + 45 + (i * 54)),
                                 (win_wt - 45, 64 + 45 + (i * 54)), 2)
                
                # vertical lines
                pygame.draw.line(win, (0, 0, 0), (45 + (i * 54),
                                                  64 + 45), (45 + (i * 54), win_ht - 64 - 45), 2)
            else:
                # horizontal lines
                pygame.draw.line(win, (0, 0, 0), (45, 64 + 45 + (i * 54)),
                                 (win_wt - 45, 64 + 45 + (i * 54)), 1)

                # vertical lines
                pygame.draw.line(win, (0, 0, 0), (45 + (i * 54),
                                                64 + 45), (45 + (i * 54), win_ht - 64 - 45))
            
        
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[col][row] != 0:
                    print_text(number_font, self.board[col][row], row*54 + 45 + 27 - 10, col*54 + 54 + 45 + 27)

        pygame.draw.rect(win, (0, 0, 0), self.solve_box, 1)
        print_text(text_font_2, "Solve", self.solve_box.x + 22, self.solve_box.y + 5)

        pygame.draw.rect(win, (0, 0, 0), self.erase_box, 1)
        print_text(text_font_2, "Eraser", self.erase_box.x + 5, self.solve_box.y + 3)

        pygame.draw.rect(win, (0, 0, 0), self.rough_box, 1)
        print_text(text_font_2, "Rough", self.rough_box.x +
                   5, self.solve_box.y + 3)

def main():

    solved_grid, grid = engine.generate_grid(50)
    engine.print_grid(solved_grid)
    # engine.print_grid(grid)

    def run_game():

        board = Board(grid)
        
        while True:
            out_events()

            board.draw(win)
            dt = fps_clock.tick(fps) / 1000
            dt *= 60

            pygame.display.update()

    while True:
        run_game()
        pass


if __name__ == "__main__":
    main()

