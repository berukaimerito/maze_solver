from graphics import Window, Maze


def main():
    num_rows = 11
    num_cols = 11
    margin = 10
    screen_x = 480
    screen_y = 480
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
