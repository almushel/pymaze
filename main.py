from maze import *

def main():
	win = Window(800, 600)
	
	maze = Maze(
		Point(1,1),
		10, 10,
		Point(25, 25),
		win
	)

	for x in range(maze.rows):
		for y in range(maze.cols):
			maze._draw_cell(x, y)


	win.wait_for_close()

main()