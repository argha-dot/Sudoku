import random

def isValid(arr, row, col, num):

    valid = True

    for i in range(0, 9):
        if arr[i][col] == num:
            valid = False

        if arr[row][i] == num:
            valid = False

    for i in range(0, 3):
        for j in range(0, 3):
            if (arr[i + row - row%3][j + col - col%3] == num):
                valid = False

    return valid


def find_empty_loc(arr):
    for i in range(0, 9):
        for j in range(0, 9):
            if arr[i][j] == 0:
                return [i, j]

    return None


def solve_grid(arr):

    loc = find_empty_loc(arr)
    
    if (loc == None):
        return True

    row, col = loc[0], loc[1]

    for num in range(1, 10):
        if (isValid(arr, row, col, num)):
            arr[row][col] = num
            if solve_grid(arr):
                return True

            arr[row][col] = 0

    return False


def print_grid(arr):
    for i in range(0, 9):
        for j in range(0, 9):
            if arr[i][j] == 0:
                print("_", end=" ")
            else:
                print(arr[i][j], end=" ")

        print("")


def generate_grid():
    global counter
    
    def fill_grid(arr):
        loc = find_empty_loc(arr)

        if (loc == None):
            return True

        row, col =  loc[0], loc[1]

        number_list = [x for x in range(1, 10)]

        random.shuffle(number_list)

        for num in number_list:
            if (isValid(arr, row, col, num)):
                arr[row][col] = num
                if fill_grid(arr):
                    return True
                
                arr[row][col] = 0

        return False

    
    def solve_(arr):
        global counter
        loc = find_empty_loc(arr)

        if (loc == None):
            counter += 1
            return True

        row, col = loc[0], loc[1]

        for num in range(1, 10):
            if (isValid(arr, row, col, num)):
                arr[row][col] = num
                if solve_(arr):
                    return True                
                arr[row][col] = 0
        
        return False


    board = [[0 for i in range(0, 9)] for j in range(0, 9)]

    counter = 1
    attempts = 40

    fill_grid(board)

    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            pass
        
        back = board[row][col]
        board[row][col] = 0

        # copy = board.copy()
        copy = []
        for r in range(0,9):
            copy.append([])
            for c in range(0,9):
                copy[r].append(board[r][c])

        counter = 0

        solve_(copy)
        if counter != 1:
            board[row][col] = back

        attempts -= 1        

    return (board)
