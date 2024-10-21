from tkinter import Canvas

from window import Window


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.p1 = point1
        self.p2 = point2
        self.x1 = point1.x
        self.x2 = point2.x
        self.y1 = point1.y
        self.y2 = point2.y

    def draw(self, canvas: Canvas, fill_color="white") -> None:
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)


class Cell:
    def __init__(self, win: Window | None = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1: float | None = None
        self._x2: float | None = None
        self._y1: float | None = None
        self._y2: float | None = None
        self._win: Window | None = win

    def draw(self, x1: float, x2: float, y1: float, y2: float, fill_color="white"):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        top_wall = Line(Point(x1, y1), Point(x2, y1))
        bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        left_wall = Line(Point(x1, y1), Point(x1, y2))
        right_wall = Line(Point(x2, y1), Point(x2, y2))
        if self.has_top_wall:
            self._win.draw_line(line=top_wall, fill_color=fill_color)
        else:
            self._win.draw_line(line=top_wall, fill_color="black")
        if self.has_bottom_wall:
            self._win.draw_line(line=bottom_wall, fill_color=fill_color)
        else:
            self._win.draw_line(line=bottom_wall, fill_color="black")
        if self.has_left_wall:
            self._win.draw_line(line=left_wall, fill_color=fill_color)
        else:
            self._win.draw_line(line=left_wall, fill_color="black")
        if self.has_right_wall:
            self._win.draw_line(line=right_wall, fill_color=fill_color)
        else:
            self._win.draw_line(line=right_wall, fill_color="black")

    def draw_move(self, to_cell: "Cell", undo=False):
        if self._win is None:
            return
        if (
            self._x1 is None
            or self._x2 is None
            or to_cell._x1 is None
            or to_cell._x2 is None
        ):
            return
        if (
            self._y1 is None
            or self._y2 is None
            or to_cell._y1 is None
            or to_cell._y2 is None
        ):
            return
        x_self_center = (self._x1 + self._x2) / 2
        y_self_center = (self._y1 + self._y2) / 2
        point_self_center = Point(x_self_center, y_self_center)

        x_to_center = (to_cell._x1 + to_cell._x2) / 2
        y_to_center = (to_cell._y1 + to_cell._y2) / 2
        point_to_center = Point(x_to_center, y_to_center)

        path = Line(point_self_center, point_to_center)
        if undo:
            color = "gray"
        else:
            color = "red"
        path.draw(self._win.canvas, fill_color=color)

    def __repr__(self):
        return f"<Cell: {self.visited} T: {self.has_top_wall} B: {self.has_bottom_wall} R: {self.has_right_wall} L: {self.has_left_wall}>"
