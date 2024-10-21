from tkinter import BOTH, Canvas, Tk


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bg="black", height=height, width=width)
        self.canvas.pack(fill=BOTH, side="top", expand=1)
        self.running = False

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.running = True
        while self.running is True:
            self.redraw()

    def close(self) -> None:
        self.running = False

    def draw_line(self, line, fill_color="white"):
        line.draw(self.canvas, fill_color=fill_color)
