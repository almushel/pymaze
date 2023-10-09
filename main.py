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

	solved = False
	solution_draw_index = 0
	solution = []
	while(win.running):
		if maze._path_index <= len(maze._paths):
			maze.draw()
		elif not solved:
			solution = maze.solve()
			solved = True
		elif solution and solution_draw_index < len(solution)-1:
			coords = solution[ solution_draw_index ]
			from_cell = maze._cells[coords.x][coords.y]
			
			coords = solution[ solution_draw_index+1 ]
			to_cell = maze._cells[coords.x][coords.y]
			
			from_cell.draw_move(to_cell)
			solution_draw_index += 1
		
		maze.draw()	
		sleep(FRAME_TIME)

main()