from tkinter import Tk, BOTH, Canvas

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	
	def __truediv__(self, val):
		# Assumes val is a scalar value
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

class Cell:
	# rect: Rectangle(x, y, width, height)
	# walls: top, right, bottom, left	
	def __init__(self, rect, window, walls=[True, True, True, True]):
		self.rect = rect	
		self.walls = walls
		self.window = window

	def draw(self, stroke_color):
		top_left = self.rect.position
		top_right = top_left + Point(self.rect.width, 0)
		bottom_left = top_left + Point(0, self.rect.height)
		bottom_right = self.rect.bottom_right

		if self.walls[0]:
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



def main():
	win = Window(800, 600)
	
	cell1 = Cell(Rectangle(25, 25, 100, 100), win, walls=[True, False, True, True])
	cell1.draw("red")

	cell2 = Cell(Rectangle(125, 25, 100, 100), win, walls=[True, True, True, False])
	cell2.draw("green")

	cell1.draw_move(cell2)

	win.wait_for_close()

main()