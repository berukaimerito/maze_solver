import time
import random
from tkinter import Tk, Canvas

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                # create a cell at position (i, j)
                cell = Cell(0, 0, 0, 0, self.win)  # will set actual coordinates in _draw_cell
                row.append(cell)
            self._cells.append(row)

        # draw cells
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cells(i, j)

    def _draw_cells(self, i, j):
        # calculate x1, y1 based on i, j, self.x1, self.y1 and cell size
        x1 = self.x1 + (j * self.cell_size_x)
        y1 = self.y1 + (i * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        # update the cells coordinates
        cell = self._cells[i][j]
        cell._Cell__x1 = x1
        cell._Cell__x2 = x2
        cell._Cell__y1 = y1
        cell._Cell__y2 = y2

        cell._draw_cell()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.2)  # Reduced sleep time for smoother animation

    def _break_entrance_and_exit(self):
        top_cell = self._cells[0][0]
        bottom_cell = self._cells[self.num_rows - 1][self.num_cols - 1]

        top_cell.has_top_wall = False
        top_cell._draw_cell()
        bottom_cell.has_bottom_wall = False
        bottom_cell._draw_cell()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        directions = ['left', 'right', 'up', 'down']
        random.shuffle(directions)  # Randomize directions to ensure a random maze

        for direction in directions:
            ni, nj = i, j  # Neighbor indices
            if direction == 'left' and j > 0:
                nj = j - 1
            elif direction == 'right' and j < self.num_cols - 1:
                nj = j + 1
            elif direction == 'up' and i > 0:
                ni = i - 1
            elif direction == 'down' and i < self.num_rows - 1:
                ni = i + 1
            else:
                continue  # Skip invalid directions

            if not self._cells[ni][nj].visited:
                # Break walls between current cell and neighbor
                self._break_walls_between(i, j, ni, nj)
                self._break_walls_r(ni, nj)

    def _break_walls_between(self, i, j, ni, nj):
        # Left
        if nj == j - 1:
            self._cells[i][j].has_left_wall = False
            self._cells[ni][nj].has_right_wall = False
        # Right
        elif nj == j + 1:
            self._cells[i][j].has_right_wall = False
            self._cells[ni][nj].has_left_wall = False
        # Up
        elif ni == i - 1:
            self._cells[i][j].has_top_wall = False
            self._cells[ni][nj].has_bottom_wall = False
        # Down
        elif ni == i + 1:
            self._cells[i][j].has_bottom_wall = False
            self._cells[ni][nj].has_top_wall = False

        # Redraw only the affected cells
        self._cells[i][j]._draw_cell()
        self._cells[ni][nj]._draw_cell()

        # Animate after the walls have been redrawn
        self._animate()

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        self._reset_cells_visited()  # Ensure visited is reset before solving
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        current_cell = self._cells[i][j]

        # Right
        if not current_cell.has_right_wall and j + 1 < self.num_cols and not self._cells[i][j + 1].visited:
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], undo=True)

        # Down
        if not current_cell.has_bottom_wall and i + 1 < self.num_rows and not self._cells[i + 1][j].visited:
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], undo=True)

        # Left
        if not current_cell.has_left_wall and j - 1 >= 0 and not self._cells[i][j - 1].visited:
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], undo=True)

        # Up
        if not current_cell.has_top_wall and i - 1 >= 0 and not self._cells[i - 1][j].visited:
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i - 1][j], undo=True)

        return False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        # Draw line with specified color
        line = canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)
        # print(f"Line ID: {line}")  # Optional debug statement

class Cell:
    def __init__(self, x1, x2, y1, y2, win, has_left_wall=True, has_right_wall=True,
                 has_top_wall=True, has_bottom_wall=True, visited=False):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.__win = win
        self.visited = visited

    def _draw_cell(self):
        # Set the cell color to black for walls
        wall_color = "black"

        # Draw the walls of the cell
        if self.has_left_wall:
            line = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__win.draw_line(line, wall_color)
        if self.has_top_wall:
            line = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__win.draw_line(line, wall_color)
        if self.has_right_wall:
            line = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__win.draw_line(line, wall_color)
        if self.has_bottom_wall:
            line = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__win.draw_line(line, wall_color)

        # If walls are broken (indicating a passage), redraw with background color
        background_color = "white"
        if not self.has_top_wall:
            line = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__win.draw_line(line, background_color)
        if not self.has_bottom_wall:
            line = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__win.draw_line(line, background_color)
        if not self.has_left_wall:
            line = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__win.draw_line(line, background_color)
        if not self.has_right_wall:
            line = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__win.draw_line(line, background_color)

    def draw_move(self, to_cell, undo=False):
        # Calculate the center of the current cell
        x1_center = (self.__x1 + self.__x2) / 2
        y1_center = (self.__y1 + self.__y2) / 2

        # Calculate the center of the target cell
        x2_center = (to_cell.__x1 + to_cell.__x2) / 2
        y2_center = (to_cell.__y1 + to_cell.__y2) / 2

        # Create a line from the center of this cell to the center of the target cell
        line = Line(Point(x1_center, y1_center), Point(x2_center, y2_center))

        # Set the color based on whether it's an undo or a normal move
        if undo:
            self.__win.draw_line(line, "gray")
        else:
            self.__win.draw_line(line, "red")

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._root_widget = Tk()
        # Set canvas background to white by adding the 'bg' parameter
        self.__canvas = Canvas(self._root_widget, width=self.width, height=self.height, bg="white")
        self.__canvas.pack()  # Packs the canvas into the window
        self._root_widget.title(f"w:{self.width}, h:{self.height}")
        self._running = True  # Initialize as True to enter the loop

        # Bind the close event properly
        self._root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root_widget.update_idletasks()
        self._root_widget.update()

    def wait_for_close(self):
        # No need to reset self._running here
        while self._running:
            self.redraw()
            time.sleep(0.1)  # Optional: add a small delay to prevent high CPU usage

    def close(self):
        self._running = False
        self._root_widget.destroy()  # Properly close the window

    def draw_line(self, ln: Line, fill_color):
        ln.draw(self.__canvas, fill_color)
        # No need to call redraw here as _animate() handles it
