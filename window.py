import turtle
import random
import time
import sys

class Grid:
    def __init__(self, size):
        if self.wrong_size(size) :
            sys.exit('Wrong value for grid size (', size, ')')
        self.size = size
        self.value = [[0 for i in range(size)] for i in range(size)]


gridSize = input("Gridsize : ")
gridSize = int(gridSize)
boardSize = 600
xvar = int(boardSize/gridSize)
yvar = int(boardSize/gridSize)

fwdSlashFlag = 0b100000
bckSlashFlag = 0b010000
horizFlag = 0b001000
vertiFlag = 0b000100
p2Flag = 0b000010
p1Flag = 0b000001
playerFlags = 0b11

colors = ["Blue", "Red"]

score = [0, 0]
rounds = 0
AI_depth = 2

def AI_player2(grid, depth) :
    max_weight = -10000
    for i in range(gridSize) :
        for j in range(gridSize) :
            if grid[i][j] == 0 :
                grid[i][j] = 2;
                tmp = eval_min(grid, depth-1)
                if tmp > max_weight :
                    #print("maximal ", i, j, tmp)
                    max_weight = tmp
                    ai_row = i
                    ai_col = j
                grid[i][j] = 0;
    play(2, ai_row+1, ai_col+1)
    check_win(grid, False)

def eval_min(grid, depth) :
    winner = check_win(grid, True)
    if depth == 0 or winner != 0 :
        return weight_eval(grid, winner)

    min_weight = 10000
    for i in range(gridSize) :
        for j in range(gridSize) :
            if grid[i][j] == 0 :
                grid[i][j] = 2;
                tmp = eval_max(grid, depth-1)
                if tmp < min_weight :
                    min_weight = tmp
                    #print("min ", i, j, tmp)
                grid[i][j] = 0;
    return min_weight
    
def eval_max(grid, depth) :
    winner = check_win(grid, True)
    if depth == 0 or winner != 0 :
        return weight_eval(grid, winner)

    max_weight = -10000
    for i in range(gridSize) :
        for j in range(gridSize) :
            if grid[i][j] == 0 :
                grid[i][j] = 2;
                tmp = eval_min(grid, depth-1)
                if tmp > max_weight :
                    max_weight = tmp
                    #print("max ", i, j, tmp)
                grid[i][j] = 0;
    return max_weight

def weight_eval(grid, winner) :
    if winner == 2 :
        return 100 - rounds
    elif winner == 1 :
        return rounds - 100
    else :
        return score[1] - score[0]
   
def get_posY(row):
    return boardSize/2 - row*yvar + yvar/2

def get_posX(col):
    return col*xvar - boardSize/2 - xvar/2

def action_col_row(x, y):
    col = (x + boardSize/2 + xvar/2) / xvar
    row = -(y - boardSize/2 - yvar/2) / yvar

    if abs(col - round(col)) > 0.2 or abs(row - round(row)) > 0.2 :
        print("Too far from grid")
    else :
        col = round(col)
        row = round(row)
        if not play(1, row, col) :
            print ("No cheating!")
        else :
            check_win(grid, False)
            AI_player2(grid, AI_depth)
            #pretty_print(grid)

def play(player, row, col) :
    gridR = row - 1
    gridC = col - 1
    if grid[gridR][gridC] == 0:
        #print(grid[gridR][gridC])
        grid[gridR][gridC] = player
        #print(grid, row, col)
        mark_board(player, row, col)
        return True
    else :
        return False

def mark_board(player, row, col):
        board.goto(get_posX(col), get_posY(row))
        board.shape("circle")
        board.color(colors[player-1])
        board.stamp()
        board.up()
   
def check_win(grid, check):
    win = 0
    score = [0, 0]
    rounds = 0
    for i in range(gridSize) :
        for j in range(gridSize) : 
            if grid[i][j] & playerFlags :
                rounds = rounds + 1
                if not grid[i][j] & vertiFlag and check_win_verti(grid, i, j, check) :
                    win = grid[i][j] & playerFlags
                    break
                if not grid[i][j] & horizFlag and check_win_horiz(grid, i, j, check) :
                    win = grid[i][j] & playerFlags
                    break
                if not grid[i][j] & bckSlashFlag and check_win_bckSlash(grid, i, j, check) :
                    win = grid[i][j] & playerFlags
                    break
                if not grid[i][j] & fwdSlashFlag and check_win_fwdSlash(grid, i, j, check) :
                    win = grid[i][j] & playerFlags
                    break
        if win != 0 : 
            break
    reset_flags(grid)
    if not check and rounds == gridSize*gridSize :
        end_game_draw()
    return win


def reset_flags(grid) :
    for i in range(gridSize) :
        for j in range(gridSize) :
            grid[i][j] = grid[i][j] & playerFlags

#should only need to check below current coordinates
def check_win_verti(grid, row, col, check) :
    i = row
    count = 0
    while(i < gridSize and (grid[i][col] & playerFlags) == (grid[row][col] & playerFlags)) :
        count = count + 1
        grid[i][col] = grid[i][col] | vertiFlag
        i = i + 1
    if count == 5 : 
        if not check :
            victory(grid[row][col] & playerFlags)
        return True
    else :
        player = (grid[row][col] & playerFlags) - 1
        score[player] = score[player] + count# * count
        return False

def check_win_horiz(grid, row, col, check) :
    j = col
    count = 0
    while(j < gridSize and grid[row][j] & playerFlags == grid[row][col] & playerFlags) :
        count = count + 1
        grid[row][j] = grid[row][j] | horizFlag
        j = j + 1
    if count == 5 :
        if not check :
            victory(grid[row][col] & playerFlags)
        return True
    else :
        player = (grid[row][col] & playerFlags) - 1
        score[player] = score[player] + count# * count
        return False

def check_win_bckSlash(grid, row, col, check) :
    j = col
    i = row
    count = 0
    while(j < gridSize and i < gridSize and grid[i][j] & playerFlags == grid[row][col] & playerFlags) :
        count = count + 1
        grid[i][j] = grid[i][j] | bckSlashFlag
        j = j + 1
        i = i + 1
    if count == 5 :
        if not check :
            victory(grid[row][col] & playerFlags)
        return True
    else :
        player = (grid[row][col] & playerFlags) - 1
        score[player] = score[player] + count# * count
        return False

def check_win_fwdSlash(grid, row, col, check) :
    j = col
    i = row
    count = 0
    while(j < gridSize and i < gridSize and grid[i][j] & playerFlags == grid[row][col] & playerFlags) :
        count = count + 1
        grid[i][j] = grid[i][j] | fwdSlashFlag
        j = j - 1
        i = i + 1
    if count == 5 :
        if not check : 
            victory(grid[row][col] & playerFlags)
        return True
    else :
        player = (grid[row][col] & playerFlags) - 1
        score[player] = score[player] + count# * count
        return False

def victory(player) :
    board.ht()
    board.goto(0, 0)
    board.color("Lightgreen")
    board.write("Player " + str(player) + " wins !", align="center", font=("Arial", 48, "normal"))
    board.exitonclick()
    sys.exit()

def end_game_draw() :
    board.ht()
    board.goto(0, 0)
    board.color("Lightgreen")
    board.write("Draw !", align="center", font=("Arial", 48, "normal"))
    board.exitonclick()
    sys.exit()

def draw_board(board):
    board.bgcolor(.55, .75, .65)
    board.up()
    board.speed(0)
    board.pensize(10)
    board.color(.1, .2, .25)
    for i in range(gridSize):
        board.setx(-boardSize/2)
        board.sety(boardSize/2 - yvar*i - yvar/2)
        board.down()
        board.forward(boardSize)
        board.up()
        board.setx(-boardSize/2 + xvar * i + xvar/2)
        board.sety(boardSize/2)
        board.down()
        board.sety(-boardSize/2)
        board.up()

def init_grid(gridSize):
    grid = [[0 for i in range(gridSize)] for i in range(gridSize)]
    return grid 
   

def main():    
    draw_board(board)
    board.Screen().onclick(action_col_row)
    #board.exitonclick()
    board.mainloop()
 
def pretty_print(grid) :
    for i in range(gridSize) :
        print(grid[i])
    print("\n")

turtle.setup(boardSize, boardSize)
board = turtle  
grid = init_grid(gridSize)
main()
