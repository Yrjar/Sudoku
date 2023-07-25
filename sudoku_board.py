from typing import Any
import numpy as np
import pygame as pg
from dataclasses import dataclass

class SudokuBoard():
    def __init__(self) -> None:
        self.board = np.array([[SudokuCell() for i in range(9)] for j in range(9)])
        self.rows = np.array([Row() for i in range(9)])
        self.cols = np.array([Col() for i in range(9)])
        self.squares = np.array([Square() for i in range(9)])

        # Set row, col, and square for each cell
        for i in range(9):
            for j in range(9):
                self.board[i][j].row = i
                self.rows[i].cells.append(self.board[i][j])

                self.board[i][j].col = j
                self.cols[j].cells.append(self.board[i][j])

                square_idx = (i // 3) * 3 + (j // 3)
                self.board[i][j].square = square_idx
                self.squares[square_idx].cells.append(self.board[i][j])


    def draw_grid(self, screen, window_size, board_size, cell_size):
        for i in range(10):
            if i % 3 == 0:
                line_width = 3
            else:
                line_width = 1
            pg.draw.line(screen, (0, 0, 0), (int(window_size*0.05), int(window_size*0.05)+i*cell_size), (int(window_size*0.05)+board_size, int(window_size*0.05)+i*cell_size), line_width)
            pg.draw.line(screen, (0, 0, 0), (int(window_size*0.05)+i*cell_size, int(window_size*0.05)), (int(window_size*0.05)+i*cell_size, int(window_size*0.05)+board_size), line_width)

    def isolate_subsets(self):
        container_list = [self.rows, self.cols, self.squares]
        for containers in container_list:
            for container in containers:
                pass

        


    def __repr__(self) -> str:
        # Print with lines between each 3x3 square
        repr_str = ''
        for i in range(9):
            for j in range(9):
                repr_str += f'{self.board[i][j]} '
                if j % 3 == 2 and j != 8:
                    repr_str += '| '
            repr_str += '\n'
            if i % 3 == 2 and i != 8:
                repr_str += '---------------------\n'

        return repr_str
    
    def __getitem__(self, key):
        return self.board[key]
    
    def __setitem__(self, key, value):
        self.board[key].value = value


class Container():
    def __init__(self) -> None:
        self.cells = []
        self.possible_values = [1,2,3,4,5,6,7,8,9]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} with cells {self.cells}'

class Row(Container):
    def __init__(self) -> None:
        super().__init__()

class Col(Container):
    def __init__(self) -> None:
        super().__init__()

class Square(Container):
    def __init__(self) -> None:
        super().__init__()



@dataclass
class SudokuCell():
    value: int = 0
    possible_values: list = None
    row: int = None
    col: int = None
    square: int = None

    def __post_init__(self):
        self.possible_values = [1,2,3,4,5,6,7,8,9]

    def __repr__(self) -> str:
        return f'{self.value}'
    
    def update(self, board: SudokuBoard) -> None:
        if self.value != 0:
            self.possible_values = []
            for i in range(9):
                if board.rows[self.row].cells[i].value == 0:
                    if self.value in board.rows[self.row].cells[i].possible_values:
                        board.rows[self.row].cells[i].possible_values.remove(self.value)
                if board.cols[self.col].cells[i].value == 0:
                    if self.value in board.cols[self.col].cells[i].possible_values:
                        board.cols[self.col].cells[i].possible_values.remove(self.value)
                if board.squares[self.square].cells[i].value == 0:
                    if self.value in board.squares[self.square].cells[i].possible_values:
                        board.squares[self.square].cells[i].possible_values.remove(self.value)
        else:
            self.possible_values = [1,2,3,4,5,6,7,8,9]
            for i in range(9):
                if board.rows[self.row].cells[i].value != 0:
                    if board.rows[self.row].cells[i].value in self.possible_values:
                        self.possible_values.remove(board.rows[self.row].cells[i].value)
                if board.cols[self.col].cells[i].value != 0:
                    if board.cols[self.col].cells[i].value in self.possible_values:
                        self.possible_values.remove(board.cols[self.col].cells[i].value)
                if board.squares[self.square].cells[i].value != 0:
                    if board.squares[self.square].cells[i].value in self.possible_values:
                        self.possible_values.remove(board.squares[self.square].cells[i].value)
            
    
if __name__ == '__main__':
    board = SudokuBoard()
    print(board)
    board.isolate_subsets()


