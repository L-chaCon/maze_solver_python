import random
from time import sleep

from cell import Cell, Line, Point
from window import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        seed: int | None = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells: list[Cell | []] = []

        self._create_cells()
        self._break_entrance_and_exit()

        if seed is not None:
            random.seed(seed)

        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        self._cells = []
        for i in range(self.num_rows):
            row: list[Cell | []] = []
            for j in range(self.num_cols):
                row.append(Cell(win=self.win))
            self._cells.append(row)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j) -> None:
        x1 = self.x1 + j * self.cell_size_x
        y1 = self.y1 + i * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        cell = self._cells[i][j]
        cell.draw(x1=x1, x2=x2, y1=y1, y2=y2)
        self._animate

    def _animate(self) -> None:
        if self.win is None:
            return
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        first_cell = self._cells[0][0]
        last_cell = self._cells[-1][-1]

        first_cell.has_top_wall = False
        last_cell.has_bottom_wall = False

        self._draw_cell(0, 0)
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_go = []
            if i > 0 and not self._cells[i - 1][j].visited:
                to_go.append((i - 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                to_go.append((i, j - 1))
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                to_go.append((i + 1, j))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                to_go.append((i, j + 1))

            if len(to_go) == 0:
                self._draw_cell(i, j)
                return

            where_to_go = random.randrange(0, len(to_go))
            index_to_go = to_go[where_to_go]
            if index_to_go[0] == i - 1:
                cell.has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            if index_to_go[0] == i + 1:
                cell.has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            if index_to_go[1] == j - 1:
                cell.has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            if index_to_go[1] == j + 1:
                cell.has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False

            self._break_walls_r(index_to_go[0], index_to_go[1])

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        if i > 0 and not cell.has_top_wall and not self._cells[i - 1][j].visited:
            cell.draw_move(self._cells[i - 1][j])
            solved = self._solve_r(i - 1, j)
            if solved:
                return True
            else:
                cell.draw_move(self._cells[i - 1][j], undo=True)
        if (
            i < self.num_rows - 1
            and not cell.has_bottom_wall
            and not self._cells[i + 1][j].visited
        ):
            cell.draw_move(self._cells[i + 1][j])
            solved = self._solve_r(i + 1, j)
            if solved:
                return True
            else:
                cell.draw_move(self._cells[i + 1][j], undo=True)
        if j > 0 and not cell.has_left_wall and not self._cells[i][j - 1].visited:
            cell.draw_move(self._cells[i][j - 1])
            solved = self._solve_r(i, j - 1)
            if solved:
                return True
            else:
                cell.draw_move(self._cells[i][j - 1], undo=True)
        if (
            j < self.num_cols - 1
            and not cell.has_right_wall
            and not self._cells[i][j + 1].visited
        ):
            cell.draw_move(self._cells[i][j + 1])
            solved = self._solve_r(i, j + 1)
            if solved:
                return True
            else:
                cell.draw_move(self._cells[i][j + 1], undo=True)
        return False
