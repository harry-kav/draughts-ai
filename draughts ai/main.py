import pygame

from draughts.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLUE
from draughts.board import Board
from draughts.game import Game
from minimax.minimax import minimax

#initialising display window
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("draughts")

def get_row_col_from_mouse(pos):
	x, y = pos
	row = y // SQUARE_SIZE
	col = x //SQUARE_SIZE

	return row, col

def main():
	run = True
	game_clock = pygame.time.Clock()
	game = Game(WIN)

	#piece = board.get_piece(0,1)
	#board.move(piece, 4,3)

	while run == True:
		game_clock.tick(FPS)
		
		if game.turn == WHITE:
			value, new_board = minimax(game.get_board(), 3, WHITE, game)
			print(value)
			game.ai_move(new_board)

			#set the allowed moves on the first turn
		#if len(game.allowed_moves) <1:
		#	game.allowed_moves = game.get_allowed_moves()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				row, col = get_row_col_from_mouse(mouse_pos)

				#if game.turn == BLUE:
				game.select(row,col)
		
		game.update()	

main()