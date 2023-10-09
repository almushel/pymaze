import random
from copy import copy
from time import sleep
from tkinter import Tk, BOTH, Canvas

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	
	def __truediv__(self, val):
		return Point(self.x / val, self.y / val)
	
	def __str__(self):
		return f"Point(x: {self.x}, y: {self.y})"
	
	def __repr__(self):
		return f"Point({self.x}, {self.y})"


class Line:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def draw(self, canvas, fill_color):
		canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color)
		canvas.pack()

class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	@property
	def position(self):
		return Point(self.x, self.y)
	
	@property
	def dimensions(self):
		return Point(self.width, self.height)
	
	@property
	def bottom_right(self):
		return self.position + self.dimensions
	
	def __str__(self):
		return f"Rectangle(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height})"
	
	def __repr__(self):
		return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"

class Cell:
	def __init__(self, rect, window=None, walls=[True, True, True, True]):
		self.rect = copy(rect)
		self.walls = copy(walls)
		self.window = window
		self.visited = False

	def set_wall_by_name(self, name, val):
		names = ["top", "right", "bottom", "left"]
		if name in names:
			self.walls[ names.index(name) ] = bool(val)
		else:
			raise Exception("Invalid wall name")

	def draw(self, stroke_color):
		top_left = self.rect.position
		top_right = top_left + Point(self.rect.width, 0)
		bottom_left = top_left + Point(0, self.rect.height)
		bottom_right = self.rect.bottom_right

		if self.walls[0]: # top
			self.window.draw_line(Line(top_left, top_right), stroke_color)
		if self.walls[1]: # right
			self.window.draw_line(Line(top_right, bottom_right), stroke_color)
		if self.walls[2]: # bottom
			self.window.draw_line(Line(bottom_right, bottom_left), stroke_color)
		if self.walls[3]: # left
			self.window.draw_line(Line(bottom_left, top_left), stroke_color)

	def draw_move(self, to_cell, undo=False):
		stroke_color = "green"
		if undo: stroke_color = "red"

		start 	= self.rect.position + (self.rect.dimensions/2)
		end 	= to_cell.rect.position + (to_cell.rect.dimensions/2)

		self.window.draw_line(Line(start, end), stroke_color)
	
	def __str__(self):
		return f"Cell( rect: {str(self.rect)}, Walls: {self.walls})"

class MazeNode:
	def __init__(self, x, y, parent):
		self.parent = parent
		self.x = x
		self.y = y
		self.neighbors = []
		self.children = []


class Maze:
	def __init__(self, position, rows, cols, cell_size, window=None, seed=None):
		self.position = position
		self.rows = rows
		self.cols = cols
		self.cell_size = cell_size
		self.window = window
		self._create_cells()
		self._break_entrance_and_exit()
		if seed:
			random.seed(seed)

		self._paths = self._create_path_r(0,0)
		self._path_index = 0
		self._reset_cells_visited()
	
	def _create_cells(self):
		self._cells = []

		rect = Rectangle(
			self.position.x, self.position.y,
			self.cell_size.x, self.cell_size.y
		)
		for x in range(self.cols):
			self._cells.append([])
			for y in range(self.rows):
				self._cells[x].append(
					Cell(rect, self.window)
				)
				rect.y += self.cell_size.y
			rect.x += self.cell_size.x
			rect.y = self.position.y
	
	def _break_entrance_and_exit(self):
		self._cells[0][0].set_wall_by_name("top", False)
		self._cells[self.cols-1][self.rows-1].set_wall_by_name("bottom", False)

	def _create_path_r(self, x, y, path=[]):
		path.append(Point(x,y))
		current_cell = self._cells[x][y]
		current_cell.visited = True

		directions = {
			"left": 	Point(x-1,y),
			"top": 		Point(x,y-1),
			"right": 	Point(x+1,y),
			"bottom": 	Point(x,y+1),
		}
		keys = []

		for key in directions:
			d = directions[key]
			if (d.x in range(self.cols) and d.y in range(self.rows)): 
				keys.append(key)
		
		while len(keys):
			key = random.choice(keys)
			nx, ny = directions[key].x, directions[key].y
			next_cell = self._cells[nx][ny]
			
			if next_cell.visited:
				keys.remove(key)
				continue

			current_cell.set_wall_by_name(key, False)

			if key == "left": key = "right"
			elif key == "right": key = "left" 
			elif key == "top": key = "bottom"
			elif key == "bottom": key = "top"

			self._cells[nx][ny].set_wall_by_name(key, False)

			self._create_path_r(nx, ny, path)
		return path
	
	def _reset_cells_visited(self):
		for x in self._cells:
			for y in x:
				y.visited = False
	
	def get_cell_exits(self, x, y):
		result = []

		neighbors = [
			Point(x,y-1),
			Point(x+1,y),
			Point(x,y+1),
			Point(x-1,y)
		]

		cell = self._cells[x][y]
		for w in range(len(cell.walls)):
			nw = neighbors[w]
			if nw.x < 0 or nw.x >= self.cols or nw.y < 0 or nw.y >= self.rows: 
				continue
			elif not cell.walls[w]:
				result.append(nw)

		return result

	def solve(self):
		result = []
		current = MazeNode(0,0, None)
		current.neighbors = self.get_cell_exits(0,0)
		found = False

		while (current):
			if current.x == self.cols-1 and current.y == self.rows-1:
				found = True
			
			if (found):
				result.append(Point(current.x, current.y))
				current = current.parent
			elif current.neighbors:
				n = current.neighbors.pop()
				neighbor = self._cells[n.x][n.y]
				if not neighbor.visited:
					next_node = MazeNode(n.x, n.y, current)
					
					neighbor.visited = True
					
					next_node.neighbors = self.get_cell_exits(next_node.x, next_node.y)
					current.children.append(next_node)
					current = next_node
			else:
				current = current.parent
		if not found:
			return None
		
		result.reverse()
		return result

	def _draw_cell(self, x, y):
		self._cells[x][y].draw("black")

	def draw(self):
		if self._path_index < len(self._paths):
			next_cell = self._paths[self._path_index]
			self._draw_cell(next_cell.x, next_cell.y)	
			self._path_index += 1
		
		if self._path_index == len(self._paths):
			self._path_index += 1
			for x in range(self.cols):
				for y in range(self.rows):
					self._draw_cell(x,y)
		self.window.redraw()


class Window:
	def __init__(self, width, height):
		self.__root = Tk()
		self.__root.title = "Maze Solver"
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.canvas = Canvas(width=width, height=height)
		self.canvas.pack()
		self.running = True
	
	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()

	def close(self):
		self.running = False

	def draw_line(self, line, fill_color):
		line.draw(self.canvas, fill_color)
