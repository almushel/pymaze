import unittest
from maze import Maze, Point

CELL_SIZE = 10

class Tests(unittest.TestCase):

	def test_maze_create_cells(self):
		cols = 12
		rows = 10
		m1 = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
		self.assertEqual(len(m1._cells), cols)
		self.assertEqual(len(m1._cells[0]), rows)

	def test_window_optional(self):
		cols = 15
		rows = 27
		m = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
		self.assertEqual(len(m._cells), cols)
		self.assertEqual(len(m._cells[0]), rows)
		self.assertEqual(m.window, None)

if __name__ == "__main__":
	unittest.main()