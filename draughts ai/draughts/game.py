import pygame
from .constants import BLUE, WHITE, SQUARE_SIZE
from .board import Board

class Game:
	def __init__(self, win):
		self._init()
		self.win = win

	def update(self):
		self.board.draw(self.win)
		self.draw_valid_moves(self.valid_moves)
		pygame.display.update()

	def _init(self):
		self.selected_piece = None
		self.board = Board()
		self.turn = BLUE
		self.valid_moves = {}
		self.allowed_moves = self.get_allowed_moves(self.board)

	def reset(self):
		self._init()

	def select(self,row,col):
		#if a piece has been selected, move it to the newly selected spot
		if self.selected_piece:
			result = self._move(row,col)

			#if move was invalid call the method again, but without a selected piece
			if not result:
				self.selected_piece = None
				self.select(row,col)

		piece = self.board.get_piece(row,col)

		if piece != 0 and piece.colour == self.turn:
			self.selected_piece = piece
			self.valid_moves = self.board.get_valid_moves(piece, self.allowed_moves)

			return True
		return False

	def _move(self,row,col):
		print("move")
		piece = self.board.get_piece(row,col)
		#if the selected square is empty, and is a valid move, then move the piece and change turn
		if self.selected_piece and piece == 0 and (row,col) in self.valid_moves:
			self.board.move(self.selected_piece, row, col)
			skipped = self.valid_moves[(row,col)]
			print(str(skipped))

			if skipped:
				print("removing piece")
				self.board.remove(skipped)

			self.change_turn()
		else:
			return False

		#self.change_turn()
		return True

	def change_turn(self):
		self.valid_moves = {}
		if self.turn == BLUE:
			self.turn = WHITE
		else:
			self.turn = BLUE

		self.allowed_moves = self.get_allowed_moves(self.board)

	def draw_valid_moves(self, moves):
		for move in moves:
			row,col = move
			pos = (col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2)
			radius = 10
			pygame.draw.circle(self.win, WHITE, pos, radius)

	def get_board(self):
		return self.board

	def ai_move(self,board):
		self.board = board
		self.change_turn()

	def get_allowed_moves(self, board):
		pieces = self.board.get_all_pieces(self.turn)

		allowed_moves = {}
		for piece in pieces:
			moves = self.board.get_valid_moves(piece)

			for move in moves:
				row, col = move
				skipped = moves[(row,col)]
				if skipped:
					allowed_moves[(row, col)] = skipped
				#print(move)
				#if self.turn == WHITE:
				#	if [BLUE] == move:
				#		b = input()
				#		allowed_moves.update(move)
				#else:
				#	if [WHITE] == move:
						
				#		allowed_moves.update(move)

		print("Allowed moves: " +str(allowed_moves))
		return allowed_moves


