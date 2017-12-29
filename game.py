#!/usr/bin/env python

from numpy import matrix
import sys
import time

class Board():

    # Board should be a n x m matix of cells that describes a flat torus  
    def __init__(self, cells=None):
        if cells is None:
            self.cells = self.from_file("board.txt")
            self.shape = self.cells.shape
        else:
            self.cells = cells
            self.shape = cells.shape

    def __str__(self):
        string = ""
        shape = self.shape
        for row in range(shape[0]):
            for i in range(shape[1]):
                cell = self.cells.item(row,i)
                string = string + str(cell) + ' '
            string = string + '\n'
        return string[:-2]

    def from_file(self, file_name):
        self.save_file = open(file_name,'r')
        rowc = 0
        board = []
        for row in self.save_file:
            board.append([])
            cellc = 0
            for cell in row[:-1]:
                board[rowc].append( Cell(rowc,cellc,bool(int(cell))) )
                cellc = cellc + 1
            rowc = rowc + 1
        return matrix(board)

    def get_neighbours(self, cell):
        # It is from the neighbours that we know we are on a torus
        my_row = cell.x
        my_col = cell.y
        row = self.shape[0] -1
        col = self.shape[1] -1
        first_row = my_row - 1
        first_col = my_col - 1
        last_row = my_row + 1
        last_col = my_col + 1

        if my_row == 0:
            first_row = row

        if my_col == 0:
            first_col = col

        if my_row == row:
            last_row = 0

        if my_col == col:
            last_col = 0

        return MooreN( [ self.cells.item(first_row,first_col), self.cells.item(first_row,my_col), self.cells.item(first_row,last_col), 
                         self.cells.item(my_row,first_col), self.cells.item(my_row,last_col), self.cells.item(last_row,first_col), 
                         self.cells.item(last_row,my_col), self.cells.item(last_row,last_col) ], cell) 


    def next_gen(self):
        board = []
        shape = self.shape
        for row in range(shape[0]):
            board.append([])
            for col in range(shape[1]):
                cell = self.cells.item(row,col)
                board[row].append( Cell( row, col , self.get_neighbours(cell).is_alive() ) )
        return Board(matrix (board))

class Cell:

    # A cell is either dead or alive and has coordinates

    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive

    def __str__(self):
        if self.alive:
            return "*"
        else:
            return " "

class MooreN:

    # Moore Neighbourhood is all eight cells surrounding a central cell
    # ***
    # * *
    # ***

    def __init__(self, cells, cell):
        self.cells = cells
        self.cell = cell

    def __str__(self):
        string = ""
        for cell in self.cells:
            string = string + str(cell) + '\n'
        return string[:-1]

    def count(self):
        count = 0
        for cell in self.cells:
            if cell.alive:
                count = count + 1
        return count

    def is_alive(self):
        if self.cell.alive:
            if self.count() == 2 or self.count() == 3:
                return True
            else:
                return False
        else:
            if self.count() == 3:
                return True
            else:
                return False


board = Board()
while True:
    print("\033[H\033[J")
    print(board)
    time.sleep(0.1)
    board = board.next_gen()


