from engine import *


def main():
    
    _game_board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                  [5, 2, 0, 0, 0, 0, 0, 0, 0],
                  [0, 8, 7, 0, 0, 0, 0, 3, 1],
                  [0, 0, 3, 0, 1, 0, 0, 8, 0],
                  [9, 0, 0, 8, 6, 3, 0, 0, 5],
                  [0, 5, 0, 0, 9, 0, 6, 0, 0],
                  [1, 3, 0, 0, 0, 0, 2, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 7, 4],
                  [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    game_board = generate_grid()

    back_up = game_board[:]

    print_grid(game_board)

    print("")
    

    n = (input())

    print("")

    if solve_grid(game_board):
        print_grid(game_board)
    else:
        print("f")

    print("")

    # print(back_up)


if __name__ == "__main__":
    main()
