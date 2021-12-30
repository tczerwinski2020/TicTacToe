import pygame
import time

WIDTH = 700
HEIGHT = 500
BACKGROUND_COLOR = (245, 213, 219)
CONTRAST_COLOR = (247,100,149)

# Prints board in formatted manner
def print_board(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == "":
				print(" ", end = "|")
			else:
				print(board[i][j],end = "|")
		print()
		print("-"*7)


# Checks to see if 3 of the same player in a row for any rows in the board
def check_row(board):
	for j in range(len(board)):
		for i in range(len(board[j])):
			if board[j][0] != board[j][i]:
				break
			if i == len(board[j])-1 and board[j][i] != "":
				return j
	return -1


# Checks to see if 3 of the same player in a column for all columns in the board
def check_col(board):
	for i in range(len(board[0])):
		for j in range(len(board)):
			if board[j][i] != board[0][i]:
				break
			if j == 2 and board[j][i] != "":
				return i
	return -1


# Checks to see if either diagnal of the board is filled with the same player
def check_diagonal(board):
	if board[0][0] == board[1][1] == board[2][2] != "":
		return 0
	if board[2][0] == board[1][1] == board[0][2] != "":
		return 2
	return -1


# Draws winner screen
def draw_winner(win, winner):
	win.fill(BACKGROUND_COLOR)
	draw_menu(win)
	label_font = pygame.font.SysFont("Gadugi", 50)
	win_label = label_font.render(winner+" wins!", True, (0,0,0))
	win.blit(win_label, (200,150))
	pygame.display.update()
	return 


# Checks all rows, cols, and diagnals of the board for a winner (3 of the same player)
def check_winner(win, board):
	win_row = check_row(board)
	if win_row != -1:
		return (0, win_row)
	win_col = check_col(board)
	if win_col != -1:
		return (1, win_col)
	win_dia = check_diagonal(board)
	if win_dia != -1:
		return (2, win_dia)
	return -1


# Draws tie screen 
def draw_tie(win):
	win.fill(BACKGROUND_COLOR)
	draw_menu(win)
	label_font = pygame.font.SysFont("Gadugi", 50)
	win_label = label_font.render("Tie Game!", True, (0,0,0))
	win.blit(win_label, (175,150))
	pygame.display.update()


# Draws menu screen
def draw_menu(win):
	global nextChar
	mouse = pygame.mouse.get_pos()
	label_font = pygame.font.SysFont("Gadugi", 50)
	tictactoe = label_font.render("Tic Tac Toe", True, (0,0,0))
	win.blit(tictactoe, (HEIGHT+10,100))
	button_font = pygame.font.SysFont("Gadugi", 35)
	nextPlayer = button_font.render(nextChar+" up next!", True, CONTRAST_COLOR)
	win.blit(nextPlayer, (550, 400))
	clear = button_font.render("Clear", True, (0,0,0))
	clear_btn = pygame.Rect(570,190,75,40)

	if 570 <= mouse[0] <= 645 and 190 <= mouse[1] <= 230:
		pygame.draw.rect(win, CONTRAST_COLOR, clear_btn)
	else:
		pygame.draw.rect(win, BACKGROUND_COLOR, clear_btn)
	win.blit(clear, (HEIGHT+75, 200))

	if winner:
		new_game = button_font.render("New Game", True, (0,0,0))
		ng_button = pygame.Rect(190,240,150,40)
		if 185 <= mouse[0] <= 335 and 235 <= mouse[1] <= 270:
			pygame.draw.rect(win, CONTRAST_COLOR, ng_button)
		else:
			pygame.draw.rect(win, BACKGROUND_COLOR, ng_button)
		win.blit(new_game, (200, 250))
	return clear_btn


# Draws the board on the screen
def draw_board(win, board):
	label_font = pygame.font.SysFont("Gadugi", 250)
	for i in range(1,4):
		box1 = pygame.Rect((HEIGHT/3)*(i-1), (HEIGHT/3)*(i-1),HEIGHT/3,HEIGHT/3)
		pygame.draw.rect(win, CONTRAST_COLOR, box1)
	box2 = pygame.Rect(0, (HEIGHT/3)*(2), HEIGHT/3, HEIGHT/3)
	pygame.draw.rect(win, CONTRAST_COLOR, box2)
	box3 = pygame.Rect((HEIGHT/3)*2, 0, HEIGHT/3, HEIGHT/3)
	pygame.draw.rect(win, CONTRAST_COLOR, box3)
	for i in range(len(board)):
		for j in range(len(board[0])):
			num = label_font.render(board[i][j], True, (0,0,0))
			win.blit(num, ((HEIGHT/3)*j+20, (HEIGHT/3)*i+10))
	for i in range(1,4):
		pygame.draw.line(win, (0,0,0), (int(HEIGHT/3)*i, 0), (int(HEIGHT/3)*i, 500), 6)
		pygame.draw.line(win, (0,0,0), (0, int(HEIGHT/3)*i), (500, int(HEIGHT/3)*i), 6)
	return


# Inserts player's move into the board and displays the result on the screen
def insert(win, board, mouse_pos):
	x = int(mouse_pos[0]//(HEIGHT/3))
	y = int(mouse_pos[1]//(HEIGHT/3))
	global nextChar
	board[y][x] = nextChar
	if nextChar == "X":
		nextChar = "O"
	else:
		nextChar = "X"
	win.fill(BACKGROUND_COLOR)
	draw_board(win, board)
	draw_menu(win)


# Returns True if the board is full (does not contain "")
def board_full(board):
	return not any("" in x for x in board)


# Main method
def main():
	global board
	global winner
	pygame.init()
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Tic-Tac-Toe")
	win.fill(BACKGROUND_COLOR)
	draw_board(win, board)
	ng_button = pygame.Rect(190,240,150,40)


	while True:
		clear_btn = draw_menu(win)		
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				if clear_btn.collidepoint(mouse_pos) or (winner and ng_button.collidepoint(mouse_pos)):
					win.fill(BACKGROUND_COLOR)
					winner = False
					board = [["","",""],
							["","",""],
							["","",""]]
					draw_board(win, board)
					draw_menu(win)
					continue
				if mouse_pos[0] < HEIGHT + 1:
					insert(win, board, mouse_pos)
					i = check_winner(win, board)
					if i != -1:
						winner = True
						draw_winner(win, board[0][i[1]])
					if board_full(board):
						winner = True
						draw_tie(win)
						
									
#global variables
board = [["","",""],
		["","",""],
		["","",""]]
nextChar = "X"
winner = False
main()