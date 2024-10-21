from maze import Maze
from window import Window


def main():
    num_rows = 24
    num_cols = 18
    margin = 10
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    # cell_size_x = 100
    # cell_size_y = 100
    win = Window(screen_x, screen_y)

    maze = Maze(
        x1=margin,
        y1=margin,
        num_rows=num_rows,
        num_cols=num_cols,
        cell_size_x=cell_size_x,
        cell_size_y=cell_size_y,
        win=win,
    )

    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
