from maze import *

SCREEN_W = 800
SCREEN_H = 600
FRAME_TIME = 1/60

def main():
	win = Window(800, 600)
	
	rows = cols = 50
	rect = Rectangle(5, 5, (SCREEN_W-10)/cols, (SCREEN_H-10)/rows)

	maze = Maze(
		rect.position,
		rows, cols,
		rect.dimensions,
		win, 42
	)

	while(win.running):
		maze.draw()
		sleep(FRAME_TIME)

main()