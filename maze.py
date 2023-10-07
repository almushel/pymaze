from numbers import Number
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
		self.walls = walls
		self.window = window

	def set_wall_by_name(self, name, val):
		names = ["top", "right", "bottom", "left"]
		if name in names:
			self.walls[ names.index(name) ] = bool(val)
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
		stroke_color="gray"
		if undo: stroke_color = "red"

		start 	= self.rect.position + (self.rect.dimensions/2)
		end 	= to_cell.rect.position + (to_cell.rect.dimensions/2)

		self.window.draw_line(Line(start, end), stroke_color)
	
	def __str__(self):
		return f"Cell( rect: {str(self.rect)}, Walls: {self.walls})"

class Maze:
	def __init__(self, position, rows, cols, cell_size, window=None):
		self.position = position
		self.rows = rows
		self.cols = cols
		self.cell_size = cell_size
		self.window = window
		self._create_cells()
	
	def _create_cells(self):
		self._cells = [[] for r in range(self.cols)]

		rect = Rectangle(
			self.position.x, self.position.y,
			self.cell_size.x, self.cell_size.y
		)
		for x in range(self.cols):
			for y in range(self.rows):
				self._cells[x].append(
					Cell(rect, self.window)
				)
				rect.y += self.cell_size.y
			rect.x += self.cell_size.x
			rect.y = self.position.y
	
	def _draw_cell(self, x, y):
		self._cells[x][y].draw("black")
		self._animate()
	
	def _animate(self):
		self.window.redraw()
		sleep(1/60)


class Window:
	def __init__(self, width, height):
		self.__root = Tk()
		self.__root.title = "Maze Solver"
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.canvas = Canvas()
		self.canvas.pack()
		self.running = False
	
	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()

	def wait_for_close(self):
		self.running = True
		while self.running:
			self.redraw()

	def close(self):
		self.running = False

	def draw_line(self, line, fill_color):
		line.draw(self.canvas, fill_color)
