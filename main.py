import sys, os
import pygame
from pygame.locals import *
import engine


def terminate():
    pygame.quit()
    sys.exit()


def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()

win_wt, win_ht = (9*16*4), (11*16*4)
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))

class Board(object):

    def __init__(self, board):
        self.board = board

    def draw(self, win):
        pass


def main():
    pygame.init()

    def run_game():
        
        while True:
            out_events()

            win.fill((64, 128, 128))

            dt = fps_clock.tick(fps) / 1000
            dt *= 60

            pygame.display.update()

    while True:
        run_game()
        pass


if __name__ == "__main__":
    main()

