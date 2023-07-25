import pygame as pg
from sudoku_board import SudokuBoard

window_width = 600
background_color = (255, 255, 255)

class SudokuGame():
    def __init__(self) -> None:
        pg.init()
        self.board = SudokuBoard()
        self.screen = pg.display.set_mode((window_width, window_width))
        self.clock = pg.time.Clock()
        self.running = True
        self.board_size = int(window_width*0.9)
        self.cell_size = int(self.board_size/9)
        self.selected_cell = None


    def draw_numbers(self):
        font = pg.font.Font('freesansbold.ttf', 32)
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value != 0:
                    text = font.render(str(self.board[i][j]), True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (int(window_width*0.05)+j*self.cell_size+int(self.cell_size/2), int(window_width*0.05)+i*self.cell_size+int(self.cell_size/2))
                    self.screen.blit(text, textRect)

    def draw_possible_values(self):
        font = pg.font.Font('freesansbold.ttf', 10)
        sub_cell_size = int(self.cell_size/3) - 3
        offsets = [-sub_cell_size, 0, sub_cell_size]
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value != 0:
                    continue
                cell_center_pos = (int(window_width*0.05)+j*self.cell_size+int(self.cell_size/2), int(window_width*0.05)+i*self.cell_size+int(self.cell_size/2))
                for k in range(9):
                    if k+1 not in self.board[i][j].possible_values:
                        continue
                    text = font.render(str(k+1), True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (cell_center_pos[0]+offsets[k%3], cell_center_pos[1]+offsets[int(k/3)])
                    self.screen.blit(text, textRect)
    
    # draw selected cell
    def draw_selected_cell(self):
        if self.selected_cell is None:
            return
        pg.draw.rect(self.screen, (0, 0, 255), (int(window_width*0.05)+self.selected_cell[1]*self.cell_size, int(window_width*0.05)+self.selected_cell[0]*self.cell_size, self.cell_size, self.cell_size), 3)


    def handle_events(self):
        for event in pg.event.get():

            # Quit game
            if event.type == pg.QUIT:
                self.running = False
                raise SystemExit
            
            # Select cell with mouse
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < int(window_width*0.05) or mouse_pos[0] > int(window_width*0.05)+self.board_size:
                    self.selected_cell = None
                    continue
                if mouse_pos[1] < int(window_width*0.05) or mouse_pos[1] > int(window_width*0.05)+self.board_size:
                    self.selected_cell = None
                    continue
                self.selected_cell = ((mouse_pos[1]-int(window_width*0.05))//self.cell_size, (mouse_pos[0]-int(window_width*0.05))//self.cell_size)

            # Keyboard input
            if event.type == pg.KEYDOWN:

                # move selected cell
                if event.key == pg.K_LEFT:
                    if self.selected_cell is None:
                        self.selected_cell = (0, 0)
                    else:
                        self.selected_cell = (self.selected_cell[0], (self.selected_cell[1]-1)%9)
                if event.key == pg.K_RIGHT:
                    if self.selected_cell is None:
                        self.selected_cell = (0, 0)
                    else:
                        self.selected_cell = (self.selected_cell[0], (self.selected_cell[1]+1)%9)
                if event.key == pg.K_UP:
                    if self.selected_cell is None:
                        self.selected_cell = (0, 0)
                    else:
                        self.selected_cell = ((self.selected_cell[0]-1)%9, self.selected_cell[1])
                if event.key == pg.K_DOWN:
                    if self.selected_cell is None:
                        self.selected_cell = (0, 0)
                    else:
                        self.selected_cell = ((self.selected_cell[0]+1)%9, self.selected_cell[1])

                # change value of selected cell
                new_value = range(1, 10)
                pg_key = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]
                for i in range(9):
                    if event.key == pg_key[i]:
                        if self.selected_cell is None:
                            continue
                        self.board[self.selected_cell[0]][self.selected_cell[1]].value = new_value[i]
                        self.board[self.selected_cell[0]][self.selected_cell[1]].update(self.board)

                # delete value of selected cell
                if event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                    if self.selected_cell is None:
                        continue
                    self.board[self.selected_cell[0]][self.selected_cell[1]].value = 0

                    # update possible values of all cells
                    for cell in self.board.board.flatten():
                        cell.update(self.board)

            


    def update(self):
        pass

    def draw(self):
        self.screen.fill(background_color)
        self.board.draw_grid(self.screen, window_width, self.board_size, self.cell_size)
        self.draw_numbers()
        self.draw_possible_values()
        self.draw_selected_cell()
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == '__main__':
    
    game = SudokuGame()
    game.run()