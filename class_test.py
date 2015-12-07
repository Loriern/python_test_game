import turtle
import math
import random
import time
import sys

class Grid:

    fwdSlashFlag = 0b100000
    bckSlashFlag = 0b010000
    horizFlag = 0b001000
    vertiFlag = 0b000100
    
    p2Flag = 0b000010
    p1Flag = 0b000001
    playerFlags = 0b11

    def __init__(self, size=10):
        self.size=size
        self.value=[[0 for i in range(size)] for i in range(size)]
    
    def setSizeFromInput():
        new_size=input("Grid size: ")
        if new_size > 4 and new_size < 20:
            self.size=new_size

class Player:
    def __init__(self, number):
        self.number=number
        self.score=0
        self.moves=[]

class Move:
    def __init__(self, row, column, player):
        self.row=row
        self.col=column
        self.player=player

class Board:
    
    colors = ["Blue", "Red"]
    board=turtle

    def __init__(self, size=600, grid=Grid()):
        self.size=size
        self.grid=grid
        self.xvar=int(size/grid.size)
        self.yvar=self.xvar

    def draw():
        board.bgcolor(.55, .75, .65)
        board.up()
        board.speed(0)
        board.pensize(10)
        board.color(.1, .2, .25)
        for i in range(self.grid.size):
            board.setx(-self.size/2)
            board.sety(self.size/2 - yvar*i - yvar/2)
            board.down()
            board.forward(self.size)
            board.up()
            board.setx(-self.size/2 + xvar * i + xvar/2)
            board.sety(self.size/2)
            board.down()
            board.sety(-self.size/2)
            board.up() 

    def get_posY(row):
        return self.size/2 - row*self.yvar + self.yvar/2

    def get_posX(col):
        return col*self.xvar - self.size/2 - self.xvar/2

    def get_col(x):
        return (x + self.size/2 + self.xvar/2)/xvar 

    def get_row(y):
        return (self.size/2 + self.yvar/2 - y)/yvar

class Game:
        click_precision=0.3
        p1=Player(1)
        p2=Player(2)

    def __init__(self, board=Board()):
        self.board=board

    def click_action(x, y):
        col = self.board.get_col(x)
        row = self.board.get_row(y)

        if abs(col - round(col)) > click_precision or abs(row - round(row)) > click_precision :
            print("Too far from grid")
        else :
            col = round(col)
            row = round(row)
            if not p1.play(row, col) :
                print ("No cheating!")
            else :
                self.check_win(grid, False)
                self.AI(p2)
                #pretty_print(grid)


