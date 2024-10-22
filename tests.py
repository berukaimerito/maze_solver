import unittest
from graphics import Maze, Window


class Tests(unittest.TestCase):
    # def test_maze_create_cells(self):
    #     window = Window(1280, 720)
    #     num_cols = 4
    #     num_rows = 4
    #     m1 = Maze(0, 0, num_rows, num_cols, 10, 10, window)
    #
    #     self.assertEqual(
    #         len(m1._cells),
    #         num_cols,
    #     )
    #     self.assertEqual(
    #         len(m1._cells[0]),
    #         num_rows,
    #     )

    # def test_break_entrance_and_exit(self):
    #     window = Window(1280, 720)
    #     num_cols = 5
    #     num_rows = 5
    #     m2 = Maze(40, 40, num_rows, num_cols, 20, 20, window)
    #     m2._break_entrance_and_exit()
    #
    #     self.assertEqual(
    #         m2._cells[0][0].has_top_wall,
    #         False
    #     )
    #     self.assertEqual(
    #         m2._cells[-1][-1].has_bottom_wall,
    #         False
    #     )
    #
    #     # Redraw and process events
    #     window.redraw()
    #     for _ in range(10):  # Process events multiple times
    #         window._root_widget.update_idletasks()
    #         window._root_widget.update()
    #
    #     # Close the window after processing
    #     window._root_widget.destroy()

    def test_reset_visited(self):
        # Test configuration
        num_cols = 6
        num_rows = 6
        margin = 40
        screen_x = 900
        screen_y = 720
        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows
        window = Window(screen_x, screen_y)

        m1 = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, window)

        m1._reset_cells_visited()

        # Verify that all cells' visited status is False
        for row in m1._cells:
            for cell in row:
                assert cell.visited == False, "Expected cell.visited to be False after reset"


if __name__ == '__main__':
    unittest.main()
