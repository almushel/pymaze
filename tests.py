import unittest
import random
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

	def test_entrance_and_exit(self):
		cols = 11
		rows = 23
		m = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
		self.assertEqual(m._cells[0][0].walls[0], False)
		self.assertEqual(m._cells[m.cols-1][m.rows-1].walls[2], False)

	def test_maze_edges(self):
		cols = random.randint(4, 50)
		rows = random.randint(4, 50)
		m = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
		
		for x in range(m.cols):
			for y in range(m.rows):
				if x == 0:
					# Entrance	
					if y == 0:
						self.assertEqual(m._cells[x][y].walls[0], False)
					# Left Wall
					else:
						self.assertEqual(m._cells[x][y].walls[3], True)
				elif x == m.cols-1:
					# Exit
					if y == m.rows-1:
						self.assertEqual(m._cells[x][y].walls[2], False)
					# Right wall
					else:
						self.assertEqual(m._cells[x][y].walls[1], True)
				# Top wall
				elif y == 0:
					self.assertEqual(m._cells[x][y].walls[0], True)
				# Bottom wall
				elif y == m.rows-1:
					self.assertEqual(m._cells[x][y].walls[2], True)

	def test_cells_unvisited(self):
		cols = 9
		rows = 27
		m = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
		for x in m._cells:
			for y in x:
				self.assertEqual(y.visited, False)

# NOTE: Recursion depth exceeded very quickly with a large maze
'''
	def test_maze_size_stress(self):
		cols = random.randint(5, 200)
		rows = random.randint(5, 200)
		m = Maze(Point(0,0), rows,cols, Point(CELL_SIZE,CELL_SIZE))
'''


if __name__ == "__main__":
	unittest.main()